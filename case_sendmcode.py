from scripts.handle_suds import HandleSuds
from scripts.handle_log import HandleLogging
from scripts.handle_excel import HandleExcel
from libs.ddt_new import ddt,data
from scripts.constants import TEST_DATAS_FILE_PATH2
from scripts.handle_context02 import Context
import unittest
import inspect


@ddt
class CaseSend(unittest.TestCase):
    """
     发送验证码用例
    """
    do_log = HandleLogging().get_logger()
    do_excel = HandleExcel(TEST_DATAS_FILE_PATH2, sheetname='sendMCode')
    case_list = do_excel.get_cases()

    @classmethod
    def setUpClass(cls):
        cls.do_log.info("\n{:=^40}".format("开始执行用例"))
        cls.send_request = HandleSuds()

    @classmethod
    def tearDownClass(cls):
        cls.do_log.info("\n{:=^40}".format("用例执行结束"))

    @data(*case_list)
    def test_sendMCode(self, one_case):
        self.do_log.info("\nRunning Testing Methon:{}".format(inspect.stack()[0][3]))
        new_data = Context.sendmcode_parameterization(one_case.data)

        res = self.send_request(url=one_case.url, api=one_case.api, data=new_data)

        actual_result = str(res)
        expect_result = one_case.expected
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