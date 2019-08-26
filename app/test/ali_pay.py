from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for
import json, os
from app.models import User, Order, db

cloud_pay = Blueprint('cloud_pay', __name__)

from alipay import AliPay

basepath = os.path.abspath(os.path.dirname(__file__))  # 当前文件所在目录
parentdir = os.path.dirname(basepath)  # 父级目录

private = os.path.join(parentdir, "certs", "app_private_key.pem")  # 私钥路径
public = os.path.join(parentdir, "certs", "app_public_key.pem")  # 公钥路径
alipay_public_test = os.path.join(parentdir, 'certs', 'zhifubaogongyao.txt')

app_private_key_string = open(private).read()
alipay_public_key_string = open(public).read()
alipay_public_test_string = open(alipay_public_test).read()

alipays = AliPay(
    appid="appid",  #支付宝appid
    app_notify_url=None,  # 默认回调url
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_test_string,
    debug=False
)


@cloud_pay.route('/alipay1', methods=['GET', 'POST'])
def ali_mobilepay():
    tradeid = request.form.get("tradeid")
    dati = Order.query.filter(Order.Trade_Number == tradeid).first()
    cost = dati.Print_Money
    cost = float(cost)

    global new_filename
    new_filename = dati.File_Name

    order_string = alipays.api_alipay_trade_wap_pay(out_trade_no=tradeid,
                                                    total_amount=cost,
                                                    subject='云打印订单',
                                                    return_url="http://xxx.com:8000/admin/people",
                                                    notify_url='http://xxx.com:8000/cloud_pay/native')
    url = "https://openapi.alipay.com/gateway.do?" + order_string
    # url = "https://openapi.alipaydev.com/gateway.do?" +order_string   #沙盒环境
    return redirect(url)



@cloud_pay.route('/alipay2', methods=['GET', 'POST'])
def ali_computerpay():
    tradeid = request.form.get("tradeid")
    dati = Order.query.filter(Order.Trade_Number == tradeid).first()
    cost = dati.Print_Money
    cost = float(cost)

    global new_filename
    new_filename = dati.File_Name

    order_string = alipays.api_alipay_trade_page_pay(out_trade_no=tradeid,
                                                    total_amount=cost,
                                                    subject='云打印订单',
                                                    return_url="http://xxx.com:8000/admin/people",
                                                    notify_url='http://xxx.com:8000/cloud_pay/native')
    url = "https://openapi.alipay.com/gateway.do?" + order_string
    # url = "https://openapi.alipaydev.com/gateway.do?" +order_string   #沙盒环境
    return redirect(url)


# 支付宝同步回调接口
@cloud_pay.route('/alipayresult1', methods=['GET', 'POST'])
def alipayresult1():
    trade_id = request.args.get("out_trade_no")
    data = request.args.to_dict()
    # sign 不能参与签名验证
    signature = data.pop("sign")

    print(json.dumps(data))
    print(signature)

    # verify
    success = alipays.verify(data, signature)
    if success:
        # result_order = Order.query.filter(Order.File_Dir == new_filename).first()
        # result_order.Print_Status = 1
        # result_order.Trade_Number = trade_id
        # db.session.add(result_order)
        # db.session.commit()
        # result = 1
        return render_template('result.html')


# 支付宝异步通知接口
@cloud_pay.route('/native', methods=['POST'])
def alipayresult2():
    trade_out_id = request.form.get("out_trade_no")
    data = request.form.to_dict()
    signature = data.pop("sign")

    success = alipays.verify(data, signature)
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        result_order = Order.query.filter(Order.Trade_Number == trade_out_id).first()
        result_order.Print_Status = 1
        db.session.add(result_order)
        db.session.commit()
        result = 1
        return "success"
