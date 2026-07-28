from . import db

class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20))          # 例如 "26 Aug"
    period = db.Column(db.String(20))       # "Morning" / "Afternoon" / "Evening"
    time = db.Column(db.String(30))         # "9:30-12:30"
    title = db.Column(db.String(100))       # 活动标题

    # 详情页字段（支持 Markdown）
    guide = db.Column(db.Text)              # 活动指南
    materials = db.Column(db.Text)          # 所需资料
    rules = db.Column(db.Text)              # 作业规则/评分标准
    extra_notes = db.Column(db.Text)        # 补充说明

    def __repr__(self):
        return f'<Activity {self.title}>'