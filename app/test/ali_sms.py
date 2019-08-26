from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import random
import json

#用的阿里sms，具体参数设置查看官方文档
client = AcsClient('string', 'string', 'default')
code = random.randrange(1000, 10000)  # 生成随机验证码



def send_sms(phpne_number,code):
    params = {
        'code': code
    }
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('PhoneNumbers', phpne_number)
    request.add_query_param('SignName', "同讯科技")
    request.add_query_param('TemplateCode', "SMS_168821509")
    request.add_query_param('TemplateParam', json.dumps(params))

    smsResponse = client.do_action(request)
    return smsResponse


def verify_code(form_code,code):
    if form_code == code:
        return True
    else:
        return False

