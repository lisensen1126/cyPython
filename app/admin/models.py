# coding:utf8
from app import db,app
from flask import request
from datetime import datetime
from passlib.apps import custom_app_context
from app.utils.md5 import md5
import time
# 后台用户模型

class adminUserList(db.Model):
    __tablename__ = "adminUserList"
    id = db.Column(db.Integer, primary_key=True,unique=True,comment='id')
    user_name=db.Column(db.String(100),comment='用户名')
    name = db.Column(db.String(100),comment='名字')
    pwd=db.Column(db.String(200),comment='密码')
    sex=db.Column(db.INT,comment='性别')#0男 1女 2保密
    email = db.Column(db.String(100), unique=True,comment='邮箱')  # 邮箱 唯一
    phone = db.Column(db.String(11), unique=True,comment='电话')  # 手机号码 唯一
    avatar=db.Column(db.TEXT(length=6553666),comment='头像') #65536设置的mysql表字段为mediumblob 可存储16M的blob
    reg_time=db.Column(db.DateTime,index=True, default=datetime.now,comment='注册时间')

    def to_json(self):
        '''返回给前端的字段'''
        return {
            'id': self.id,
            'userName': self.user_name,
            'name':self.name,
            'sex':self.sex,
            'email':self.email,
            'phone':self.phone,
            'avatar':self.avatar,
            'createTime': str(self.reg_time),
        }
    def verify_password(self, password):
        pwdMd5 = md5(password)
        if self.pwd == pwdMd5:
            print('MD5加密之后的密文比较', self.pwd, pwdMd5)
            return True
        else:
            return False

class adminUserLog(db.Model):
    __tablename__ = "adminUserLogs"
    id = db.Column(db.Integer, primary_key=True, unique=True, comment='id')
    operate_user_name = db.Column(db.String(100), comment='操作人用户名')
    operate_name = db.Column(db.String(100), comment='操作人真实姓名')
    operate_msg = db.Column(db.String(100), comment='操作日志')
    operate_time = db.Column(db.DateTime, index=True, default=datetime.now, comment='操作时间')
    __mapper_args__ = {
        "order_by": operate_time.desc()
    }
    def to_json(self):
        '''返回给前端的字段'''
        return {
            'id': self.id,
            'operateUserName': self.operate_user_name,
            'operateName':self.operate_name,
            'operateMsg':self.operate_msg,
            'operateTime':str(self.operate_time),
    }

class apiCallCount(db.Model):
    __tablename__ = "apiCallCount"
    id = db.Column(db.Integer, primary_key=True, unique=True, comment='id')
    api_name=db.Column(db.String(100), comment='接口名称')
    api_call_time = db.Column(db.DateTime, index=True, default=datetime.now, comment='接口调用时间')



