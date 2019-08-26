from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for, g, jsonify
from app.test import ali_sms
import json, random
from app.models import db, User
from app.forms import LoginForm, Register, Findpassword, Change_Password
from flask_login import login_user, current_user, logout_user, login_required

login = Blueprint(
    'login',
    __name__
)


@login.route("/register", methods=['POST', 'GET'])
def register():
    # code = random.randrange(1000, 10000)  # 生成随机验证码
    error_msg = None
    success = None
    form = Register()

    if current_user.is_authenticated:
        return redirect(url_for('admin.inded_select'))

    elif request.method == 'GET':
        phone_number = request.args.get('mobile_phone_number')
        # phone_number = form.tel.data
        if phone_number is not None:
            if ali_sms.send_sms(phone_number, ali_sms.code):
                return render_template('forms.html', error_msg=error_msg, form=form)
            else:
                error_msg = 'Failed to get the verification code!'
    elif form.validate_on_submit():
        tel = form.tel.data
        v_code = form.v_code.data
        password = form.password1.data
        if ali_sms.verify_code(v_code, ali_sms.code):
            # if 1:
            user = User(Tel_Number=tel)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login.back_login'))
        else:
            error_msg = '验证码不正确，请检查'
            return render_template('use_templates/c_register.html', error_msg=error_msg, form=form)
    return render_template('use_templates/c_register.html', form=form)


# 找回密码
@login.route("/findpassword", methods=['POST', 'GET'])
def findpassword():
    form = Findpassword()
    if form.validate_on_submit():
        tel = form.tel.data
        v_code = form.v_code.data
        password = form.password1.data
        if ali_sms.verify_code(v_code, ali_sms.code):
            user = User.query.filter_by(Tel_Number=tel).first()
            user.set_password(password)
            db.session.commit()
            return redirect(url_for('login.back_login'))
    return render_template('use_templates/c_findpassword.html', form=form)


@login.route("/login", methods=['POST', 'GET'])
def back_login():
    if current_user.is_authenticated:
        return redirect(url_for('printer.select'))

    form = LoginForm()
    # if form.validate_on_submit():
    if form.validate_on_submit():
        tel = form.tel.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(Tel_Number=tel).first()
        if user and user.validate_password(password):
            login_user(user, remember)
            return redirect(url_for('admin.inded_select'))
        return redirect(url_for('login.back_login'))
    return render_template('use_templates/c_login.html', form=form)


@login.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logout success', 'info')
    return redirect(url_for('login.back_login'))


# 修改密码
@login.route("/change_password", methods=['GET','POST'])
@login_required
def change_password():
    form = Change_Password()
    user = User.query.filter_by(Tel_Number=current_user.Tel_Number).first()
    if request.method == 'POST':
        old_password = form.old_password.data
        if user and user.validate_password(old_password):
            user.set_password(form.password1.data)
            db.session.commit()
            flash('修改成功,请使用新密码登录')
            return redirect(url_for('login.change_password'))
        else:
            error = "密码校验失败"
            return render_template('use_templates/layui_admin-info.html', form=form, user=user, error=error)
    return render_template('use_templates/layui_admin-info.html', form=form, user=user)