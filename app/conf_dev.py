# codeing:utf8

#dev数据库配置


configsDev={
    #数据库配置
    'dbName':'root',
    'dbPwd':'123',
    'dbHost':'localhost',
    'dbPort':'3306',
    'dbClass':'liss',

    #swigger配置
    'SWAGGER_TITLE':'swagger API接口文档',
    'SWAGGER_DESC':'使用<a href="https://github.com/flasgger/flasgger" target="_blank">flasgger</a>框架',

    #token 配置
    'secretKey':'1126',
    'tokenExpiration':3600*24 #60为60s 3600为1h 3600*24为1天 3600*24*365 为一年
}