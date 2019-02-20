import pymysql
def get_dbconnect():
    host_add = '192.168.0.100'
    port_num = 3306
    user_name = 'xh_tony'
    pw = 'xinhai0574'
    db = 'xh_tony'
    return pymysql.connect(host=host_add, port=port_num, user=user_name, password=pw, database=db)

def get_dbconnectYTZ():
    host_add = '192.168.0.100'
    port_num = 3306
    user_name = 'xh_ytz'
    pw = 'xinhai0574'
    db = 'xh_ytz'
    return pymysql.connect(host=host_add, port=port_num, user=user_name, password=pw, database=db)

def get_dbconnectZZZ():
    host_add = '111.231.206.138'
    port_num = 3306
    user_name = 'xh_ytz'
    pw = 'xinhai0574'
    db = 'xh_ytz'
    return pymysql.connect(host=host_add, port=port_num, user=user_name, password=pw, database=db)



