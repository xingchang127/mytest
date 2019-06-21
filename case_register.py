from scripts.handle_suds import HandleSuds
from scripts.handle_log import HandleLogging
from scripts.handle_mysql02 import HandleMysql
from scripts.handle_excel import HandleExcel
from libs.ddt_new import ddt,data
from scripts.constants import TEST_DATAS_FILE_PATH2
from scripts.handle_context02 import Context
import json
import unittest
import inspect


@ddt
class CaseRegister(unittest.TestCase):
    """
    注册用例
    """
    do_log = HandleLogging().get_logger()
    do_excel = HandleExcel(TEST_DATAS_FILE_PATH2, sheetname='register')
    case_list = do_excel.get_cases()

    @classmethod
    def setUpClass(cls):
        cls.do_log.info("\n{:=^40}".format("开始执行用例"))
        cls.send_request = HandleSuds()
        cls.handle_mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls):
        cls.handle_mysql.close()
        cls.do_log.info("\n{:=^40}".format("用例执行结束"))

    @data(*case_list)
    def test_register(self, one_case):
        self.do_log.info("\nRunning Testing Methon:{}".format(inspect.stack()[0][3]))
        new_data = Context.register_parameterization(one_case.data)

        res = self.send_request(url=one_case.url, api=one_case.api, data=new_data)
        if one_case.api.lower() == 'sendmcode' and res == 'ok':
            one_dict = json.loads(new_data, encoding='utf-8')
            Context.registing_tel = one_dict["mobile"]
            check_sql = one_case.check_sql
            if check_sql:
                check_sql = Context.registing_tel_replace(check_sql)
                mysql_data = self.handle_mysql(sql=check_sql)
                Context.verify_code = mysql_data["Fverify_code"]
        actual_result = str(res)
        expect_result = str(one_case.expected)
        try:
            self.assertEqual(expect_result, actual_result, msg="测试{}失败".format(one_case.title))
        except AssertionError as e:
            self.do_log.error("具体异常为：{}".format(e))
            self.do_excel.write_result(row=one_case.case_id + 1, actual=str(res), result='Fail')
            raise e
        else:
            self.do_excel.write_result(row=one_case.case_id + 1, actual=str(res), result='pass')


if __name__ == '__main__':
    unittest.main()