import logging
import logging.handlers
import os
import time
import json
from app import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
class logs(object):
    def __init__(self):
        self.logger = logging.getLogger("")
        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        # 创建文件目录
        logs_dir = "./app/logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.txt' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
                                                                   maxBytes=1024 * 1024 * 50,
                                                                   backupCount=5)
        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        rotatingFileHandler.setFormatter(formatter)
        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.NOTSET)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
mylog=logs()
def logReqRes(func):
    def wrapped(request,*args, **kwargs):
        mylog.debug('开始打印请求体------{}'.format(request.path))
        if 'Authorization' not in request.headers or request.headers['Authorization']=='' :
            mylog.debug('打印request中的token------{}'.format('没有token'))
        else:
            s = Serializer(app.config['SECRET_KEY'])
            data = s.loads(request.headers['Authorization'])
            mylog.debug('打印request中的token------{}'.format(request.headers['Authorization']))
            mylog.debug('打印request中的token解析完毕------{}'.format(data))
        mylog.debug('请求方式------{}'.format(request.method))
        if request.method == "GET":
            mylog.debug('请求参数------{}'.format(request.args.to_dict()))
        elif request.method == "POST":
            mylog.debug('请求参数------{}'.format(json.loads(request.get_data())))

        start_time = time.time()
        res = func(request,*args, **kwargs)
        end_time = time.time()
        mylog.debug('请求耗时------{} 秒'.format(end_time - start_time))
        mylog.debug('返回的结构------{}'.format(res))
        return res
    return wrapped