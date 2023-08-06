"""mssdk 是基于 Python 的为麦思多维科技客户服务的专用API接口"""

"""
0.0.1: 发布测试版本 v0.0.1
0.0.2: 发布测试版本 v0.0.2
"""

__version__ = '0.0.2'
__author__ = 'mssdk'


"""
for mssdk pro api
"""
from mssdk.pro.data_pro import pro_api

"""
for mssdk pro api token set
"""
from mssdk.utils.token_process import set_token
