# 用于参数化

import re
from scripts.handle_mysql02 import HandleMysql
import random


class Context:
    """
    实现参数化、反射功能
    """
    verify_code_pattern = re.compile(r'\$\{verify_code\}')  # 配置${loan_id} 的正则表达式
    not_existed_tel_pattern = re.compile(r"\$\{not_existed_tel\}")
    sms_db_name_pattern = re.compile(r"\$\{sms_db_name\}")
    sms_table_name_pattern = re.compile(r"\$\{sms_table_name\}")
    registing_tel_pattern = re.compile(r"\$\{registing_tel\}")
    user_id_pattern = re.compile(r"\$\{user_id\}")
    not_existed_uid_pattern = re.compile(r"\$\{not_existed_uid\}")
    verified_uid_pattern = re.compile(r"\$\{verified_uid\}")
    not_verified_uid_pattern = re.compile(r"\$\{not_verified_uid\}")

    @classmethod
    def not_existed_tel_replace(cls, data):
        """
        替换未注册的手机号
        :param data:
        :return:
        """
        do_mysql = HandleMysql()
        if re.search(cls.not_existed_tel_pattern, data):
            not_existed_tel = do_mysql.create_not_existed_mobile()
            data = re.sub(cls.not_existed_tel_pattern, not_existed_tel, data)
        do_mysql.close()
        return data

    # @classmethod
    # def user_id_replace(cls, data):
    #     """
    #     替换用户id
    #     :param data:
    #     :return:
    #     """
    #     do_mysql = HandleMysql()
    #     if re.search(cls.user_id_pattern, data):
    #         one_user_id = do_mysql.create_user_id()
    #         data = re.sub(cls.user_id_pattern, one_user_id, data)
    #     do_mysql.close()
    #     return data

    @classmethod
    def verify_code_replace(cls, data):
        """
        替换验证码
        :param data:
        :return:
        """
        if re.search(cls.verify_code_pattern, data):
            verify_code = str(getattr(cls, "verify_code"))
            data = re.sub(cls.verify_code_pattern, verify_code, data)  # 第二个和第三个参数一定为字符串类型
        return data

    @classmethod
    def registing_tel_replace(cls, data):
        """
        替换注册中的手机号、库名、表名、用户id
        :param data:
        :return:
        """
        if re.search(cls.registing_tel_pattern, data):
            registing_tel = getattr(cls, "registing_tel")
            user_id = str(random.randint(0,9)) + 'xc' + registing_tel
            sms_db_name = registing_tel[-2:]
            sms_table_name = registing_tel[-3]
            data = re.sub(cls.registing_tel_pattern, registing_tel, data)
            data = re.sub(cls.user_id_pattern, user_id, data)
            data = re.sub(cls.sms_db_name_pattern, sms_db_name, data)
            data = re.sub(cls.sms_table_name_pattern, sms_table_name, data)
        return data

    @classmethod
    def not_verified_uid_replace(cls, data):
        do_mysql = HandleMysql()
        if re.search(cls.not_verified_uid_pattern, data):
            not_verified_uid = do_mysql.create_not_verified_uid()
            data = re.sub(cls.not_verified_uid_pattern, str(not_verified_uid), data)
        do_mysql.close()
        return data

    @classmethod
    def verified_uid_replace(cls, data):
        do_mysql = HandleMysql()
        if re.search(cls.verified_uid_pattern, data):
            verified_uid = do_mysql.create_verified_uid()
            data = re.sub(cls.verified_uid_pattern, str(verified_uid), data)
        do_mysql.close()
        return data


    @classmethod
    def not_existed_uid_replace(cls, data):
        do_mysql = HandleMysql()
        if re.search(cls.not_existed_uid_pattern, data):
            not_existed_uid = do_mysql.create_not_existed_uid()
            data = re.sub(cls.not_existed_uid_pattern, str(not_existed_uid), data)
        do_mysql.close()
        return data

    @classmethod
    def sendmcode_parameterization(cls, data):
        """
        实现发送验证码功能的参数化
        :return:
        """
        # 先替换未注册的手机号
        data = cls.not_existed_tel_replace(data)

        return data

    @classmethod
    def register_parameterization(cls, data):
        """
        实现注册功能的参数化
        :return:
        """
        data = cls.not_existed_tel_replace(data)
        data = cls.registing_tel_replace(data)
        data = cls.verify_code_replace(data)
        # data = cls.user_id_replace(data)

        return data


    @classmethod
    def verify_parameterization(cls, data):
        """
        实名认证的参数化
        """
        data = cls.not_existed_uid_replace(data)
        data = cls.not_verified_uid_replace(data)
        data = cls.verified_uid_replace(data)
        return data

    @classmethod
    def bind_parameterization(cls, data):
        """
        绑定银行卡的参数化
        :param data:
        :return:
        """
        data = cls.not_existed_uid_replace(data)

        return data


if __name__ == '__main__':
    target_str1 = '{"mobilephone": "${not_existed_tel}", "pwd": "123456", "regname": "KeYou"}'
    target_str2 = 'SELECT Fverify_code FROM sms_db_${sms_db_name}.t_mvcode_info_${sms_table_name} WHERE Fmobile_no = ${registing_tel};'
    one_context = Context()
    Context.registing_tel = '13886426524'
    print(one_context.register_parameterization(target_str1))
    print(one_context.registing_tel_replace(target_str2))

