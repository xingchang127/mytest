import os

# __file__固定变量,os.path.abspath(__file__) 获取当前文件的路径
# 获取项目根目录  使用大写比较规范
# os.path.dirname（文件路径） 获取文件路径的目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取测试数据datas所在目录的路径 os.path.join 用于拼接路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')

# 获取配置文件configs所在的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')

LOGS_DIR = os.path.join(BASE_DIR, 'logs')

CASES_DIR = os.path.join(BASE_DIR, 'cases')

REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

CONFIG_DIR_PATH = os.path.join(CONFIGS_DIR,  'test.conf')

TEST_DATAS_FILE_PATH = os.path.join(DATAS_DIR, 'cases.xlsx')

TEST_DATAS_FILE_PATH2 = os.path.join(DATAS_DIR, 'cases01.xlsx')

LOGS_FILE_PATH = os.path.join(LOGS_DIR, 'case.log')

ROTATING_LOGS_FILE_PATH = os.path.join(LOGS_DIR, 'case_log')

CONFIG_USE_ACCOUNTS_PATH = os.path.join(CONFIGS_DIR, 'user_accounts.conf')