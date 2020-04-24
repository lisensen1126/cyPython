from app import db
from app.admin.models import apiCallCount
def recordCallTimes(func):
    def wrapped(request,*args, **kwargs):
        # print('记录接口请求',request.path)
        return_dict = {'status': '200', 'msg': 'token验证成功', 'flag': True, 'data': {}}
        record=apiCallCount(
            api_name=request.path,
        )
        db.session.add(record)
        db.session.commit()
        return func(request, *args, **kwargs)
    return wrapped