from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app import app
def generate_auth_token(obj):
    s = Serializer(app.config['SECRET_KEY'], expires_in=app.config["tokenExpiration"])
    # print('生成的token',str(s.dumps(obj), encoding="utf-8"))
    return str(s.dumps(obj), encoding="utf-8")
def verify_auth_token(func):
    def wrapped(request,*args, **kwargs):
        # print('aaaaaa',request.headers)
        return_dict = {'status': '200', 'msg': 'token验证成功', 'flag': True, 'data': {}}
        if 'Authorization' not in request.headers:
            #如果请求头里不带token直接失败返回
            return_dict['msg'] = '未获取到token请联系管理员'
            return_dict['flag'] = False
            return return_dict
        #解析token
        headerToken = request.headers['Authorization']
        s = Serializer(app.config['SECRET_KEY'])
        # print('header中的token',headerToken)
        try:
             data = s.loads(headerToken)
             # print('token解析成功,', data)
             return func(request,*args, **kwargs)
        except SignatureExpired:
            return_dict['msg'] = 'token失效,请重新登录'
            return_dict['flag'] = False
            return return_dict  # valid token, but expired
        except BadSignature:
             # print('token is invalid')
             return_dict['msg']='身份验证失败，请重新登录'
             return_dict['flag'] = False
             return return_dict  # invalid token
    return wrapped