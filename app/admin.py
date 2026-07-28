from flask_admin.contrib.sqla import ModelView
from . import db
from .models import Activity

class ActivityAdmin(ModelView):
    column_list = ['day', 'period', 'time', 'title']
    form_columns = ['day', 'period', 'time', 'title',
                    'guide', 'materials', 'rules', 'extra_notes']
    form_widget_args = {
        'guide': {'rows': 6},
        'materials': {'rows': 4},
        'rules': {'rows': 6},
        'extra_notes': {'rows': 4},
    }
    column_searchable_list = ['title']

def register_admin(admin_instance):
    """将 ActivityAdmin 注册到给定的 admin 实例"""
    admin_instance.add_view(ActivityAdmin(Activity, db.session))