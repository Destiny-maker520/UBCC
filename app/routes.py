from flask import Blueprint, render_template
from .models import Activity
import markdown

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/camp')
def camp():
    activities = Activity.query.order_by(Activity.day, Activity.period).all()
    # 按天分组
    days = {}
    for act in activities:
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