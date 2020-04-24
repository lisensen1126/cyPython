# coding:utf8
from app import db

# 前台用户模型
class feUserList(db.Model):
    __tablename__ = "feUserList"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))





