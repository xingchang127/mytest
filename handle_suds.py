from suds.client import Client
from scripts.handle_log import do_log
import json

class HandleSuds:
    """
    处理soap请求
    """
    def __call__(self, url, api, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                do_log.error(e)
                do_log.error("{}不是json格式！".format(data))
                data = eval(data)
        client = Client(url=url)
        if api.lower() == 'sendmcode':
            try:
                res = client.service.sendMCode(data)
            except Exception as e:
                return e.fault.faultstring
            else:
                return res.retInfo

        if api.lower() == 'userregister':
            try:
                res = client.service.userRegister(data)
            except Exception as e:
                return e.fault.faultstring
            else:
                return res.retInfo

        if api.lower() == 'verifyuserauth':
            try:
                res = client.service.verifyUserAuth(data)
            except Exception as e:
                return e.fault.faultstring
            else:
                return res.retInfo

        if api.lower() == 'bindbankcard':
            try:
                res = client.service.bindBankCard(data)
            except Exception as e:
                return e.fault.faultstring
            else:
                return res.retInfo


if __name__ == '__main__':
    url1 = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
    url2 = "http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
    data = '{"client_ip": "192.168.100.1", "tmpl_id": 1, "mobile": 13812345678}'
    data2 = '{"client_ip": "", "tmpl_id": 1, "mobile": 13812345678}'
    data3 = '{"uid": "128736676748", "pay_pwd": "123456", "mobile": "18971382054", "cre_id": "42112719920127889X",' \
            ' "user_name": "畅", "cardid": "6226190601554557", "bank_type": 1001, "bank_name": "民生银行", "bank_area": "", "bank_city": ""}'
    data4 = '{"uid": "", "true_name": "畅畅", "cre_id": "42112719920127889X"}'
    res = HandleSuds()(url1, 'sendMCode', data)
    res2 = HandleSuds()(url1, 'sendMCode', data2)
    res3 = HandleSuds()(url2, 'bindBankCard', data3)
    res4 = HandleSuds()(url2, 'verifyUserAuth', data4)
    print(res)
    print(res2)
    print(res3)
    print(res4)
