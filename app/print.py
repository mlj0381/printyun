from app import app, db
import click
from app.models import User
from flask import render_template


# 微信
@app.route('/vx')
def vx_form():
    return render_template('use_templates/stamp_vx.html')


# 普通照片
@app.route('/pphoto')
def pphoto_form():
    return render_template('use_templates/stamp_pphoto.html')


# 联系客服
@app.route('/service')
def sercvice_form():
    return render_template('use_templates/stamp_service.html')


# 身份证照
@app.route('/sphoto')
def sphoto_form():
    return render_template('use_templates/stamp_sphoto.html')


# 文本打印
@app.route('/text')
def text_form():
    return render_template('use_templates/stamp_text.html')


# 优惠专区
@app.route('/todi')
def todi_format():
    return render_template('use_templates/stamp_todi.html')


# 首页
@app.route('/toindex')
def toindex_form():
    return render_template('use_templates/stamp_toIndex.html')


#
@app.route('/user')
def user_form():
    return render_template('use_templates/stamp_user.html')


@app.route('/zphoto')
def zphoto_form():
    return render_template('use_templates/stamp_zphoto.html')


# 初始化数据库命令
@app.cli.command()
@click.option('--tel_number', prompt=True, help='tel_number')
@click.option('--password', prompt=True, confirmation_prompt=True, help='password')
def initdb(tel_number, password):
    db.create_all()
    click.echo('init db')
    admin = User(
        Tel_Number=tel_number,
        Role='admin'
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
