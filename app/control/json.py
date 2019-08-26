from flask import Blueprint, request, redirect, url_for, jsonify
import datetime, json, requests, qrcode, time, os
from app.utils import query_status, sign
from flask_login import login_required, current_user
from app.models import User, Order, db
from PIL import Image

jsons = Blueprint(
    'jsons',
    __name__
)


# 支付的 信息
@jsons.route('/js_pay', methods=['POST'])
@login_required
def js_pay():
    if request.method == 'POST':
        data = request.form
        trideid = data['tradeid']
        query = Order.query.filter(Order.Trade_Number == trideid).first()

        pay_data = {
            'name': str(query.File_Name),
            'pay_type': data['pay_type'],
            'price': str(query.Print_Money),
            'order_id': str(data['order_id']),
            'expire': 3600,
            'order_uid': str(data['order_uid']),
            'notify_url': 'http://xxx.com/jsons/native',   #请求回调，自己修改
        }

        # 将 参数 转为散列值
        pay_data['sign'] = sign(
            pay_data['name'],
            pay_data['pay_type'],
            pay_data['price'],
            pay_data['order_id'],
            pay_data['notify_url'],
            '55ab2edb80e34ae3bee47b4b32c7e1e5'
        )
        # 访问网站并传递参数
        print('\n请求数据: ', pay_data)
        resp = requests.post('https://xorpay.com/api/pay/xxxx', data=pay_data)  #微信支付使用xorpay
        if resp.status_code == 200:
            json_resp = json.loads(resp.text)
            print('\n得到的数据：', json_resp)
            print('\n得到的数据：', json_resp['info']['qr'])
            img = qrcode.make(json_resp['info']['qr'])
            Image.Image.save(img, 'app/static/pay_qrcode/' + data['pay_type']+data['tradeid'] + '.jpg')
            return jsonify({'url': data['pay_type']+data['tradeid'], 'aoid': json_resp['aoid']})
        else:
            return redirect(url_for('printer.select'))
    else:
        return jsonify({'mas': 'error-pay'})


@jsons.route('/native', methods=['GET', 'POST'])
def native_url():
    if request.method == "POST":
        requ = dict(request.form)
        aoid = requ['aoid']
        time.sleep(3)
        queryStatus = query_status(aoid)
        if queryStatus['status'] in ['payed', 'success']:
            order = Order.query.filter(Order.Trade_Number == requ['order_id'][6:]).first()
            order.Print_Status = 1
            db.session.add(order)
            db.session.commit()
            return 'success'
        else:
            pass


@jsons.route('/delete', methods=['GET', 'POST'])
def delete_data():
    if request.method == "POST":
        quer = request.form
        g_id = quer['trade_id'][6:]
        new_filename = quer['new_filename']
        os.remove('app/static/Upload_Files/' + new_filename)
        filename = quer['filename']
        try:
            os.remove('app/static/Upload_Files/BeforeSwitchFile/' + filename)
        except:
            pass
        one = Order.query.filter(Order.Trade_Number == g_id).first()
        db.session.delete(one)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        pass


@jsons.route('/query_status', methods=['POST'])
def query_statu():
    time.sleep(6)
    if request.method == 'POST':
        quer = request.form
        aoid = quer['aoid']
        resp = requests.get('https://xorpay.com/api/query/' + aoid)
        msg = json.loads(resp.text)
        if msg['status'] == 'success':
            return jsonify({'quey_status': 'success'})
        else:
            return jsonify({'quey_status': 'no'})
    else:
        pass


@jsons.route('/date_times', methods=['GET', 'POST'])
# @login_required
def querys():
    form = request.form
    tel_number = form['tel_num']
    date_time = form['date_time']
    page = int(form['page'])
    per_page = int(form['limit'])
    if current_user.Role == 'admin':
        if tel_number == '' and date_time == '':
            Order_date_tel = []
            dati = Order.query
            num = dati.count()
            pagination = dati.paginate(page=page,per_page=per_page)
            item = pagination.items
            for i in item:
                Order_date_tel.append(i.to_json())
            return {'code': 0, 'msg': '', 'count': num , 'data': Order_date_tel}

        elif tel_number != '' and date_time == '':
            Order_date_tel = []
            user = User.query.filter(User.Tel_Number == tel_number).first()
            if user:
                try:
                    dati = Order.query.filter(Order.User_Id == user.Id)
                    pagination = dati.paginate(page=int(page), per_page=int(per_page))
                    num = dati.count()
                    item = pagination.items
                    for i in item:
                        Order_date_tel.append(i.to_json())
                    return {'code': 0, 'msg': '', 'count': num , 'data': Order_date_tel}
                except AttributeError as e:
                    return {'code': 404, 'msg': '请检验请求接口的数据', 'error': e}

                except TypeError as e:
                    return {'code': 404, 'msg': '无此信息', 'error': e}

        elif tel_number == '' and date_time != '':
                try:
                    Order_date_tel = []
                    date_time_date = datetime.datetime.strptime(date_time, '%Y-%m-%d').date()
                    dati = Order.query.filter(Order.Born_Date_Day == date_time_date)
                    num = dati.count()
                    pagination = dati.paginate(page=int(page), per_page=int(per_page))
                    item = pagination.items
                    for i in item:
                        Order_date_tel.append(i.to_json())
                    return {'code': 0, 'msg': '', 'count': num , 'data': Order_date_tel}
                except AttributeError as e:
                    return {'code': 404, 'msg': '请检验请求接口的数据', 'error': e}

                except TypeError as e:
                    return {'code': 404, 'msg': '无此信息', 'error': e}

        # 如果数据库中没有该数据将会报错
        else:
            try:
                Order_date_tel = []
                date_time_date = datetime.datetime.strptime(date_time, '%Y-%m-%d').date()
                user = User.query.filter(User.Tel_Number == tel_number).first()
                if user:
                    dati = Order.query.filter(Order.User_Id == user.Id , Order.Born_Date_Day == date_time_date)
                    num = dati.count()
                    pagination = dati.paginate(page=int(page), per_page=int(per_page))
                    item = pagination.items
                    for i in item:
                        Order_date_tel.append(i.to_json())
                    return {'code': 0, 'msg': '', 'count': num , 'data': Order_date_tel}
                else:
                    return {'code': 404, 'msg': '无此信息'}
            except AttributeError as e:
                return {'code': 404, 'msg': '请检验请求接口的数据', 'error': e}

            except TypeError as e:
                return {'code': 404, 'msg': '无此信息', 'error': e}
    else:
        if date_time == '':
            Order_date_tel = []
            dati = Order.query.filter(Order.User_Id == current_user.Id)
            num = dati.count()
            pagination = dati.paginate(page=page, per_page=per_page)
            item = pagination.items
            for i in  item:
                Order_date_tel.append(i.to_json())
            return {'code': 0, 'msg': '', 'count': num , 'data': Order_date_tel}
        else:
            try:
                Order_date_tel = []
                date_time_date = datetime.datetime.strptime(date_time, '%Y-%m-%d').date()
                dati = Order.query.filter(Order.User_Id == current_user.Id , Order.Born_Date_Day == date_time_date)
                num = dati.count()
                pagination = dati.paginate(page=int(page), per_page=int(per_page))
                item = pagination.items
                for i in item:
                    Order_date_tel.append(i.to_json())
                return {'code': 0, 'msg': '', 'count': num , 'data': Order_date_tel}
            except AttributeError as e:
                return {'code': 404, 'msg': '请检验请求接口的数据', 'error': e}

            except TypeError as e:
                return {'code': 404, 'msg': '无此信息', 'error': e}