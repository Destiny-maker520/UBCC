from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Activity
import markdown
from sqlalchemy import case

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/camp')
def camp():
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
        if 'O-Campus' in act.title:
            link = url_for('main.o_campus')
        elif 'O-Hong' in act.title or '香港游' in act.title or 'O-HK' in act.title:
            link = url_for('main.o_hk')
        elif '西环' in act.title or 'O-西环' in act.title:
            link = url_for('main.o_saiwan')
        else:
            link = url_for('main.activity_detail', id=act.id)
        # 给每个活动添加 link 属性
        act.link = link
        days.setdefault(act.day, []).append(act)
    return render_template('camp.html', days=days)

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

@bp.route('/o-campus')
def o_campus():
    return render_template('o_campus.html')

@bp.route('/o-hk')
def o_hk():
    return render_template('o_hk.html')

@bp.route('/o-saiwan')
def o_saiwan():
    return render_template('o_saiwan.html')

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