from app import app,db,auth,authMethods
from app.admin.models import adminUserList,adminUserLog
from app.utils.addAdminLogs import addLogs
from flask_sqlalchemy import Pagination
from flask_mail import Mail,Message
from flask import jsonify,g,Response,make_response
from app.utils.logUtil import logReqRes
from app.utils.logUtil import mylog
import json
import datetime
import time
import hashlib
import xlwt
import io
from io import StringIO
from app.utils.tokenUtils import verify_auth_token,generate_auth_token
from app.utils.recordCallTimes import recordCallTimes
from app.utils.md5 import md5
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '278092588@qq.com'
app.config['MAIL_PASSWORD'] = 'xohlblaevabncabc'
app.config['MAIL_DEFAULT_SENDER']='278092588@qq.com'
mail = Mail(app)
md = hashlib.md5()
#删除用户
@verify_auth_token
@recordCallTimes
@logReqRes
def deleteUser(request,id):
    return_dict = {'status': '200', 'msg': '删除用户成功', 'flag': True, 'data': []}
    print('aa',id)
    try:
        # 有id去查询
        if id:
            deleteUser = adminUserList.query.get(id)
            if deleteUser:
                # 查到数据 进行删除
                db.session.delete(deleteUser)
                db.session.commit()
                userLogs = adminUserLog(
                    operate_name=deleteUser.name,
                    operate_user_name=deleteUser.user_name,
                    operate_msg='删除了账号  id: {id}, 姓名: {name}, 用户名 : {userName},'.format(id=deleteUser.id,name=deleteUser.name,userName=deleteUser.user_name)
                )
                addLogs(userLogs)
            else:
                # 查不到数据
                return_dict['msg'] = '删除用户失败,未根据id查询到用户'
                return_dict['flag'] = False
        else:
            # 没id直接返回
            return_dict['msg'] = '缺少id字段'
            return_dict['flag'] = False
    except Exception as err:
        db.session.rollback()
    return return_dict

#用户登录
@logReqRes
def login(request):
    return_dict = {'status': '200', 'msg': '登录成功', 'flag': True, 'data': {}}
    get_data = request.args.to_dict()
    userName = get_data.get('userName')
    passWord = get_data.get('passWord')

    print('aaaa', userName, passWord)
    loginUser = adminUserList.query.filter_by(user_name=userName).first()
    if loginUser:
        # 有该用户
        userData = loginUser.to_json()
        # 删除头像字段，防止用该用户生成的token过大
        userData.pop('avatar')
        if loginUser.verify_password(passWord):
            print('密码正确')
            return_dict['data'] = {
                'userInfo':userData,
                'token':generate_auth_token(userData)
            }
            userLogs = adminUserLog(
                operate_name=loginUser.name,
                operate_user_name=loginUser.user_name,
                operate_msg='登录账号{}'.format(loginUser.user_name)
            )
            addLogs(userLogs)
        else:
            return_dict['flag'] = False
            return_dict['msg'] = '用户名或密码错误'

    else:
        # 该用户不存在
        return_dict['flag'] = False
        return_dict['msg'] = '该用户不存在'
    return return_dict

#获取操作日志
@verify_auth_token
@recordCallTimes
@logReqRes
def getLogsList(request):
    requestData = request.args.to_dict()
    currentPage = int(requestData.get('currentPage'))
    pageSize = int(requestData.get('pageSize'))
    if pageSize > 20:
        pageSize = 15
    return_dict = {'status': '200', 'msg': '获取日志信息成功', 'flag': True, 'data': {}}
    searchAdminUserLogPagination = adminUserLog.query.paginate(page=currentPage, per_page=pageSize)
    searchAdminUserLogList = []
    # print('查到的数据',json.dumps(searchAdminUserLogPagination.items))
    for item in searchAdminUserLogPagination.items:
        searchAdminUserLogList.append(item.to_json())
    return_dict['data'] = {
        'logsList': searchAdminUserLogList,
        'total': searchAdminUserLogPagination.total,
        'currentPage': searchAdminUserLogPagination.page,
        'pageSize': searchAdminUserLogPagination.per_page,
        'pages': searchAdminUserLogPagination.pages
    }
    return return_dict

#获取后台用户的列表(支持分页)
@verify_auth_token
@recordCallTimes
@logReqRes
def getadminUserList(request):
    return_dict = {'status': '200', 'msg': '查询成功', 'flag':True, 'data': {}}
    requestData=request.args.to_dict()
    print('1',requestData)
    currentPage=int(requestData.get('currentPage'))
    pageSize=int(requestData.get('pageSize'))
    userName=requestData.get('userName')
    phone=requestData.get('phone')
    print(currentPage,pageSize,userName,phone)
    if pageSize>20:
        pageSize=15
    foundUserPagination=Pagination
    if userName:
        #通过用户名查询
        print('通过用户名查询',userName)
        foundUserPagination = adminUserList.query.filter(adminUserList.user_name.like("%" + userName + "%")).order_by(adminUserList.reg_time.desc()).paginate(page=currentPage,per_page=pageSize)  # 通过时间排序 倒排序
    elif phone:
        print('通过电话号码查询', phone)
        foundUserPagination = adminUserList.query.filter(adminUserList.phone.like("%" + phone + "%")).order_by(adminUserList.reg_time.desc()).paginate(page=currentPage,per_page=pageSize)  # 通过时间排序 倒排序
    else:
        foundUserPagination = adminUserList.query.order_by(adminUserList.reg_time.desc()).paginate(page=currentPage, per_page=pageSize)  # 通过时间排序 倒排序
        print('tt',type(foundUserPagination))
    # page_data =           User.query.order_by(User.addtime.desc()).paginate(page=page, per_page=10)
    # foundUserArr=adminUserList.query.order_by(adminUserList.id).all()#通过id排序 默认正排序
    foundUserList=[]
    print('foundUserArr',foundUserPagination.items,foundUserPagination.total)
    if(len(foundUserPagination.items)):
        for item in foundUserPagination.items:
            # print('toJson',item.to_json())
            # itemData = {'id': item.id,  'userName':item.user_name,'name': item.name,'sex':item.sex, 'email': item.email, 'phone': item.phone,
            #             'createTime': str(item.reg_time)}
            foundUserList.append(item.to_json())
        return_dict['data'] = {
            'userList':foundUserList,
            'total':foundUserPagination.total,
            'currentPage':foundUserPagination.page,
            'pageSize':foundUserPagination.per_page,
            'pages':foundUserPagination.pages
        }
        print('222',return_dict)
    else:
        return_dict['msg'] = '未查询到数据'
        return_dict['flag'] = False

    return jsonify(return_dict)

#注册用户
@recordCallTimes
@logReqRes
def addAdminUser(request):
    return_dict = {'status': '200', 'msg': '添加用户成功', 'flag':True, 'data': {}}
    print('request.get_data()',request.get_data())
    requestData=json.loads(request.get_data())
    print('requestData',requestData)
    user=adminUserList(
        name=requestData['name'],
        user_name=requestData['userName'],
        email=requestData['email'],
        phone=requestData['phone'],
        sex=int(requestData['sex']),
    )
    user.pwd=md5(requestData['passWord'])
    ifexistUser = adminUserList.query.filter_by(user_name=requestData['userName']).first()
    ifexistUserTel = adminUserList.query.filter_by(phone=requestData['phone']).first()
    ifexistUserEmai = adminUserList.query.filter_by(email=requestData['email']).first()
    #如果数据库中有该用户，则禁止再添加
    if ifexistUser:
        return_dict['msg'] = '添加用户失败,该用户已存在'
        return_dict['flag'] = False
        return return_dict
    if ifexistUserTel:
        return_dict['msg'] = '添加用户失败,该手机号码已注册'
        return_dict['flag'] = False
        return return_dict
    if ifexistUserEmai:
        return_dict['msg'] = '添加用户失败,该邮箱已注册'
        return_dict['flag'] = False
        return return_dict
    try:
        print('333',user.pwd)
        db.session.add(user)
        db.session.commit()
        currentUser = adminUserList.query.filter_by(user_name=requestData['userName']).first()
        reg_user = currentUser.to_json()
        return_dict['msg'] = '注册用户成功,用户名:{userName}'.format(userName=reg_user['userName'])
        return_dict['data'] = reg_user
    except Exception as err:
        print('errr',err)
        db.session.rollback()
        return_dict['msg'] = '添加用户失败{}'.format(err)
        return_dict['flag'] = False
    return return_dict

#上传头像
@verify_auth_token
@recordCallTimes
def uploadHeadImage(request):
    return_dict = {'status': '200', 'msg': '上传头像成功', 'flag': True, 'data': []}
    requestData = json.loads(request.get_data())
    # print('request.FILES',requestData)
    print('print request', requestData.get('userName'))

    currentUser=adminUserList.query.filter_by(user_name=requestData['userName']).first()
    print('translate data type',type(requestData.get('avatarImg')))
    # currentUser.head_img=requestData.get('avatarImg').encode(encoding='utf-8')
    currentUser.avatar = requestData.get('avatar')
    # print('fix after type',type(currentUser.avatar))
    # currentUser.head_img=bytes('abc', encoding='utf8')
    # print('111', type(currentUser.avatar),currentUser.avatar)
    # currentUser.head_img=requestData.get('avatarImg').encode(encoding='utf-8')
    # print('2222222222',str(currentUser.head_img).encode(encoding='utf-8'))
    # print('111',type(str(currentUser.head_img).encode(encoding='utf-8')))
    try:
        print('start add head img')
        db.session.add(currentUser)
        print('start add head img1')
        db.session.commit()
        print('start add head img2')
        currentUserNew = adminUserList.query.get(currentUser.id)
        print('start add head img3',currentUserNew)
        userData = currentUserNew.to_json()
        return_dict['data'] = userData
    except Exception as err:
        print('eeeeeeeeeee',err)
        db.session.rollback()
        return_dict['msg'] = '上传头像失败,请稍后再试'+str(err)
        return_dict['flag'] = False
    # print('_______________________',return_dict)
    return return_dict

#发送邮件

@verify_auth_token
@recordCallTimes
@logReqRes
def sendEmail():
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emailBody='测试自动发送邮件，老婆爱你呦~ {nowTime}'.format(nowTime=nowTime)
    message = Message(subject='晨阳亲启', recipients=['153757949@qq.com'], body=emailBody)
    try:
        mail.send(message)
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'

#获取我的信息
@verify_auth_token
@recordCallTimes
@logReqRes
def getMyInfo(request,id=None):
    return_dict = {'status': '200', 'msg': '获取我的信息成功', 'flag': True, 'data': []}
    # print('id',id)
    myInfo= adminUserList.query.get(id)
    # print('myInfo',myInfo)
    if myInfo:
        #查找到我的信息
        myInfoObj=myInfo.to_json()
        return_dict['data']=myInfoObj
        return return_dict
    else:
        return_dict['msg']='未查询到用户信息'
        return_dict['flag']=False
        return return_dict

@verify_auth_token
@recordCallTimes
@logReqRes
def getApiStatus(request):
    return_dict = {'status': '200', 'msg': '获取api接口成功', 'flag': True, 'data': []}
    # print('id', request)
    return return_dict

def getMd5(request):
    requestData = request.args.to_dict()
    print(requestData)
    str=requestData.get('str')
    return md5(str)

def downloadAdminUserListExcel(request):
    searchResult=adminUserList.query.all()
    arr=[]
    if searchResult:
        output = io.BytesIO()
        book = xlwt.Workbook(encoding='utf8')  # 创建Workbook，相当于创建Excel
        sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)
        sheet.write_merge(0, 0, 0, 6)
        # 设置对齐方式
        alignment = xlwt.Alignment()  # Create Alignment
        # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
        alignment.horz = 0x02
        # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
        alignment.vert = 0x01
        # 设置背景颜色
        pattern = xlwt.Pattern()  # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = 5  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...

        # 设置背景颜色
        patternRed = xlwt.Pattern()  # Create the Pattern
        patternRed.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        patternRed.pattern_fore_colour = 21 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...

        #设置字体
        fontHeader = xlwt.Font()
        # 字体类型
        fontHeader.name = 'name Times New Roman'
        # 字体颜色
        fontHeader.colour_index = 3
        # 字体大小，11为字号，20为衡量单位
        fontHeader.height = 20 * 11
        # 字体加粗
        fontHeader.bold = True

        # 设置头部样式
        styleHeader = xlwt.XFStyle()
        styleHeader.font=fontHeader
        styleHeader.pattern = pattern  # Add Pattern to Style
        styleHeader.alignment = alignment  # Add Alignment to Style

        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 1000
        sheet.row(1).height_mismatch = True
        sheet.row(1).height = 600
        sheet.write(0, 0, '用户列表(导出时间{})'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), styleHeader)

        # 设置字段单元格样式
        styleHead = xlwt.XFStyle()
        styleHead.alignment = alignment

        # 设置字段单元格样式
        styleCell = xlwt.XFStyle()
        styleCell.alignment = alignment


        sheet.col(0).height=8000
        sheet.col(0).width = 2500 #设置单元格的宽度
        sheet.col(1).width = 5000  # 设置单元格的宽度
        sheet.col(2).width = 3000  # 设置单元格的宽度
        sheet.col(3).width = 3000  # 设置单元格的宽度
        sheet.col(4).width = 3000  # 设置单元格的宽度
        sheet.col(5).width = 3000  # 设置单元格的宽度
        sheet.col(6).width = 6000  # 设置单元格的宽度
        sheet.write(1, 1, '', styleHead)
        sheet.write(1, 0,'用户id',styleHead) #给第0行插入值
        sheet.write(1, 1, '用户名',styleHead)
        sheet.write(1, 2, '姓名',styleHead)
        sheet.write(1, 3, '性别',styleHead)
        sheet.write(1, 4, '邮箱',styleHead)
        sheet.write(1, 5, '电话',styleHead)
        sheet.write(1, 6, '注册时间',styleHead)
        count=int()
        for index,item in enumerate(searchResult):
            index+=2
            count=index
            sheet.write(index, 0, item.id,styleCell)
            sheet.write(index, 1, item.user_name,styleCell)
            sheet.write(index, 2, item.name,styleCell)
            if int(item.sex) == 0:
                sheet.write(index, 3, '男',styleCell)
            elif int(item.sex) == 1:
                sheet.write(index, 3, '女',styleCell)
            else:
                sheet.write(index, 3, '保密',styleCell)
            sheet.write(index, 4, item.email,styleCell)
            sheet.write(index, 5, item.phone,styleCell)
            sheet.write(index, 6, str(item.reg_time),styleCell)
        # 合并第count+1行和count+1的第0列到第六列
        sheet.write_merge(count+1, count+1, 0, 6)
        sheet.row(count+1).height_mismatch = True
        sheet.row(count+1).height = 600
        sheet.write(count+1, 0, '总计{}人(查询范围{}到{})'.format(len(searchResult),'今天','明天'), styleHeader)


        #通过浏览器下载到客户端
        book.save(output)
        output.seek(0)
        resp = make_response(output.getvalue())
        output.close()#关掉流
        resp.headers["Content-Disposition"] = "attachment; filename={}.xlsx".format(time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time())))
        resp.headers['Content-Type'] = 'application/x-xlsx'

        #生成之后直接保存在服务器端
        # book.save('D:\\{}.xlsx'.format(time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))))
    return resp




