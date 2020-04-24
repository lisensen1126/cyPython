# coding:utf8
from . import admin
from app import app,auth
from flask import request
from flasgger import swag_from
from flask_cors import CORS
from app.admin import logic
from app.utils import flasgger
from app.utils.handleError import myError

CORS(app) #全局跨域


@admin.route('/sendEmail', methods=["GET"])
def sendEmail():
    return logic.sendEmail(request)

@admin.route('/getadminUserList', methods=["GET"])
def getadminUserList():

    return logic.getadminUserList(request)

@admin.route('/regAdminUser', methods=["POST"])
@swag_from('../utils/flasgger/regAdminUser.yml')
def addAdminUser():

    return logic.addAdminUser(request)

@admin.route('/uploadHeadImage',methods=["POST"])
def uploadHeadImage():
    return logic.uploadHeadImage(request)

#登录接口
@admin.route( "/login", methods=["GET"])
@swag_from('../utils/flasgger/login.yml')
def login():
    return logic.login(request)

#获取我的信息接口
@admin.route( "/getMyInfo/<int:id>", methods=["GET"])
@swag_from('../utils/flasgger/getMyInfo.yml')
def getMyInfo(id=None):

    return logic.getMyInfo(request,id)

#删除用户接口
@admin.route( "/deleteUser/<int:id>",methods=["DELETE"])
def deleteUser(id=None):
    return logic.deleteUser(request,id)

#日志记录系统
@admin.route( "/adminUserLogs", methods=["GET"])
def getLogList():
    return logic.getLogsList(request)

@admin.route( "/apiStatus", methods=["GET"])
def getApiStatus():
    return logic.getApiStatus(request)

@admin.route( "/md5", methods=["GET"])
@swag_from('../utils/flasgger/md5.yml')
def getmd5():
    return logic.getMd5(request)

@admin.route( "/downloadAdminUserListExcel", methods=["GET"])
def downloadAdminUserListExcel():
    return logic.downloadAdminUserListExcel(request)


