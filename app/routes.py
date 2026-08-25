from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Activity
import markdown
from sqlalchemy import case

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/activity/<int:id>')
def activity_detail(id):
    act = Activity.query.get_or_404(id)
    # 将 Markdown 转为 HTML（供模板渲染）
    act.guide_html = markdown.markdown(act.guide) if act.guide else ''
    act.materials_html = markdown.markdown(act.materials) if act.materials else ''
    act.rules_html = markdown.markdown(act.rules) if act.rules else ''
    act.extra_notes_html = markdown.markdown(act.extra_notes) if act.extra_notes else ''
    return render_template('activity_detail.html', act=act)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/case-materials')
def case_materials():
    return render_template('case_materials.html')

@bp.route('/opening')
def opening():
    return render_template('opening.html')

@bp.route('/night-tour')
def night_tour():
    return render_template('night_tour.html')

@bp.route('/o-campus')
def o_campus():
    return render_template('o_campus.html')

@bp.route('/o-hk')
def o_hk():
    return render_template('o_hk.html')

@bp.route('/o-saiwan')
def o_saiwan():
    return render_template('o_saiwan.html')

@bp.route('/summer-chat')
def summer_chat():
    return render_template('summer_chat.html')

@bp.route('/game-night')
def game_night():
    return render_template('game_night.html')

@bp.route('/camp')
def camp():
    from sqlalchemy import case
    from flask import url_for

    # 自定义时段排序
    period_order = case(
        (Activity.period == 'Morning', 1),
        (Activity.period == 'Afternoon', 2),
        (Activity.period == 'Evening', 3),
        else_=4
    )
    activities = Activity.query.order_by(Activity.day, period_order).all()
    days = {}
    for act in activities:
        # 根据活动标题决定跳转链接
        title = act.title or ''
        if 'O-Campus' in title:
            link = url_for('main.o_campus')
        elif 'O-Hong' in title or '香港游' in title or 'O-HK' in title:
            link = url_for('main.o_hk')
        elif '西环' in title or 'O-西环' in title:
            link = url_for('main.o_saiwan')
        elif '开营' in title or '破冰' in title or 'Case培训' in title:
            link = url_for('main.opening')
        elif '太平山' in title or '维港' in title:
            link = url_for('main.night_tour')
        elif '小组作业' in title or 'Mini Case' in title:
            link = url_for('main.case_materials')
        elif '仲夏夜聊' in title or 'Career Talk' in title:
            link = url_for('main.summer_chat')
        elif '跨组娱乐夜' in title or 'Game Night' in title:
            link = url_for('main.game_night')
        else:
            link = url_for('main.activity_detail', id=act.id)
        act.link = link
        days.setdefault(act.day, []).append(act)
    return render_template('camp.html', days=days)

# 登录页面
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        group = request.form.get('group')
        captain = request.form.get('captain')

        # 验证逻辑
        valid_groups = ['黑芝麻豆花星冰乐', '牛奶红豆冰', '杨枝甘露', '咖喱鱼蛋', '鸡蛋仔', '刘译楠', '冰火菠萝油', 'PIC']
        valid_captains = {
            '黑芝麻豆花星冰乐': '朱茜媛',
            '牛奶红豆冰': '杨舒祁',
            '杨枝甘露': '魏舒娴',
            '咖喱鱼蛋': '惠梓萌',
            '鸡蛋仔': '刘昕然',
            '凤梨包': '刘译楠',
            '冰火菠萝油': '王安诺',
            'PIC': 'UBCC2026'
        }

        if group in valid_groups and valid_captains.get(group) == captain:
            session['logged_in'] = True
            session['group'] = group
            session['captain'] = captain
            return redirect(url_for('main.index'))
        else:
            error = '组别或队长姓名错误，请重试。'
            return render_template('login.html', error=error)

    return render_template('login.html')

# 登出
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 这里和 config.py 里的密码保持一致
        if username == 'admin' and password == 'ubcc2026hui':
            session['admin_logged_in'] = True
            return redirect(url_for('admin.index'))
        else:
            error = '用户名或密码错误，请重试。'
    return render_template('admin/login.html', error=error)