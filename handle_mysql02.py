import pymysql
import random
from scripts.handle_config import config


class HandleMysql:
    """
    处理mysql
    """
    def __init__(self):
        self.conn = pymysql.connect(host=config("mysql2", "host"),
                               user=config("mysql2", "user"),
                               password=config("mysql2", "password"),
                               # db=config("mysql", "db"),
                               port=config("mysql2", "port"),
                               charset=config("mysql2", "charset"),
                               cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def __call__(self, sql, args=None, is_more=False):
        """

        :param sql: sql语句，字符类型
        :param arg: sql语句的参数，为序列类型
        :param is_more: False or True
        :return: 字典类型或者嵌套字典的列表
        """
        self.cursor.execute(sql, args=args)
        self.conn.commit()

        if is_more:
            result = self.cursor.fetchall()
        else:
            result = self.cursor.fetchone()

        return result

    @staticmethod    # 定义静态方法，与对象无关的方法，无需使用到self参数
    def create_mobile():
        """
        随机生成11位手机号
        :return:
        """
        start_mmobile = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                         "150", "151", "152", "153", "155", "156", "157", "158", "159",
                         "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
        start_num = random.choice(start_mmobile)     # random.choice方法参数为序列类型
        one_str = "0123456789"
        end_num = "".join(random.sample(one_str, 8))    # random.sample(one_str, 8)字符串随机中取八个（8个列表）
        return start_num + end_num

    # @staticmethod
    # def  create_user_id():
    #     """
    #     随机生成用户id
    #     :return:
    #     """
    #     str1 = 'xc'
    #     str2 = '12345678'
    #     str3 = "".join(random.sample(str2, 6))
    #     return str1 + str3

    def is_existed_mobile(self, mobile):
        """
        判断手机号是否存在数据库中
        :param mobile:待判断的手机号，为字符串
        :return: True or False
        """
        sql = "SELECT * FROM user_db.t_user_info WHERE FMobile = %s;"
        if self(sql, args=(mobile, )):           # 这里的self相当于do_mysql对象,调用__call__方法
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        """
        生成未注册的手机号
        :return:
        """
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed_mobile(one_mobile):
                break
        return one_mobile

    def create_verified_uid(self):
        """
        生成已认证的uid
        :return:
        """
        sql = 'SELECT Fuid  FROM user_db.t_user_auth_info;'
        one_existed_uid = self(sql=sql)["Fuid"]
        return one_existed_uid

    def create_not_existed_uid(self):
        """
        生成不存在的uid
        :return:
        """
        sql = 'SELECT Fuid FROM user_db.t_user_info ORDER BY Fuid LIMIT 1;'
        one_not_existed_uid = self(sql=sql)["Fuid"] - 1
        return one_not_existed_uid

    def create_not_verified_uid(self):
        """
        生成未认证的uid
        :return:
        """
        sql = 'SELECT Fuid FROM user_db.t_user_info WHERE Fuid NOT in (SELECT Fuid  FROM user_db.t_user_auth_info);'
        one_not_registed_uid = self(sql=sql)["Fuid"]
        return one_not_registed_uid

    def close(self):
        """
        关闭连接
        :return:
        """
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    sql_1 = "SELECT * FROM user_db.t_user_info;"
    do_myql = HandleMysql()
    print(do_myql(sql=sql_1))
    do_myql.close()