# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import mysql.connector
from flasgger import Swagger
from app.env import env
from app.conf_dev import configsDev
from app.conf_prod import configsProd
from datetime import timedelta
from flask_httpauth import HTTPBasicAuth,HTTPAuth
auth = HTTPBasicAuth()
authMethods=HTTPAuth()
configs={}
if env=='dev':
   configs=configsDev
if env=='prod':
    configs=configsProd
app = Flask(__name__)

swagger_config = Swagger.DEFAULT_CONFIG
# print('swagger_config',swagger_config)
swagger_config['title'] = configs['SWAGGER_TITLE']    # 配置大标题
swagger_config['description'] = configs['SWAGGER_DESC']   # 配置公共描述内容
# swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
# swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
# swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
# swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'
swagger = Swagger(app,config=swagger_config)
# print('swagger_config1',swagger_config)
dbUrl="mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8mb4".format(configs['dbName'], configs['dbPwd'], configs['dbHost'], configs['dbPort'], configs['dbClass'])
app.config["SQLALCHEMY_DATABASE_URI"] =dbUrl
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = configs['secretKey']
app.config["tokenExpiration"]=configs['tokenExpiration']

app.debug = True
db = SQLAlchemy(app)

from app.cyFE import fe as fe_blueprint
from app.admin import admin as admin_blueprint
app.register_blueprint(fe_blueprint,url_prefix="/fe")
app.register_blueprint(admin_blueprint,url_prefix="/admin")



