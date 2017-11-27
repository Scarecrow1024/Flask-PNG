from . import db
from datetime import datetime

class Png(db.Model):
    __tablename__ = 'png'
    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(64), unique=True, default=False)
    bianhao = db.Column(db.String(64), unique=True, default=False)
    title = db.Column(db.String(128), default='')
    url = db.Column(db.String(128), default='')
    local_url = db.Column(db.String(128), default='')
    cdn_url = db.Column(db.String(128), default='')
    cat = db.Column(db.Integer, default=1)
    cat_1 = db.Column(db.Integer, default=0)
    cat_2 = db.Column(db.Integer, default=0)
    dpi = db.Column(db.String(8), default='')
    img = db.Column(db.String(64), default='')
    view = db.Column(db.Integer, default=0)
    down = db.Column(db.Integer, default=0)
    fav = db.Column(db.Integer, default=0)
    size = db.Column(db.String(16), default=0)
    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default='')
    format = db.Column(db.String(4), default='')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    attr = db.Column(db.String(128), default='')
    is_spider = db.Column(db.Integer, default=0)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), default=False)
    avatar = db.Column(db.String(128), default=False)
    auth_key = db.Column(db.String(128), default=False)
    access_token = db.Column(db.String(128), default=False)
    status = db.Column(db.Integer, default=1)
    reg_ip = db.Column(db.String(32), default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

class User_qq(db.Model):
    __tablename__ = 'user_qq'
    id = db.Column(db.Integer, primary_key=True)
    qq_openid = db.Column(db.String(64), default=False)
    uid = db.Column(db.Integer, default=False)

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    qq = db.Column(db.String(12), default=False)
    email = db.Column(db.String(32), default=False)
    password = db.Column(db.String(32), default=False)
    type = db.Column(db.Integer, default=1)
    _id = db.Column(db.String(128), default=False)
    max_down = db.Column(db.Integer, default=1)
    current_down = db.Column(db.Integer, default=0)
    cookie = db.Column(db.Text, default=False)
    status = db.Column(db.Integer, default=0)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def getOne(self):
        res = self.query.filter_by(status=1).first()
        return res

class PngCollect(db.Model):
    __tablename__ = 'png_collect'
    id = db.Column(db.Integer, primary_key=True)
    png_id = db.Column(db.Integer, default=False)
    uid = db.Column(db.Integer, default=False)

    @staticmethod
    def collectAdd(self, png_id, uid):
        res = self.query.filter_by(png_id=png_id, uid=uid).first()
        if res is not None:
            return False
        else:
            self.png_id = png_id
            self.uid = uid
            db.session.add(self)
            db.session.commit()
            return self.id

    @staticmethod
    def getCollect(self, uid):
        res = self.query.filter_by(uid=uid).all()
        return res

    @staticmethod
    def delCollect(self, png_id):
        res = self.query.filter_by(png_id=png_id).delete()
        return res