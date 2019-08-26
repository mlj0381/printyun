# -*- coding: utf-8 -*-

import datetime, os, time

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'User'  

    Id = db.Column(db.Integer(), primary_key=True)
    Tel_Number = db.Column(db.String(255), nullable=False)
    # Password = db.Column(db.String(255), nullable=False)
    Password_Hash = db.Column(db.String(128))
    Register_Date = db.Column(db.Date, default=datetime.date.today())
    Role = db.Column(db.String(128), default='guest', nullable=False)
    Orders = db.relationship('Order', backref='User', lazy='dynamic')

    def get_id(self):
        return self.Id

    def set_password(self, password):
        self.Password_Hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.Password_Hash, password)

    @staticmethod
    def query_all(tel_num, page=1):
        activites = User.query.filter_by(Tel_Number=tel_num).first().Orders
        if tel_num != '':
            # activites = activites.filter(User.Tel_Number.like('%' + tel_num + '%'))
            return activites.paginate(
                page, per_page=current_app.config['POST_PER_PAGE']
            )



class Order(db.Model):
    __tablename__ = 'Order'

    Id = db.Column(db.Integer(), primary_key=True)
    File_Dir = db.Column(db.String(255), nullable=False)
    File_Name = db.Column(db.String(255))  # 文件原始名字
    Born_Date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)  # 创建时间
    Born_Date_Day = db.Column(db.Date, default=datetime.date.today())  # 创建日期
    Time_Way = db.Column(db.Integer())  # 打印时间规划方式，自由排队
    Print_Date = db.Column(db.Date)  # 打印时间点 *
    Print_Place = db.Column(db.String(255), nullable=False)
    Print_pages = db.Column(db.Integer())  # 每份页数  *
    Print_Copies = db.Column(db.Integer())  # 份数
    Print_Direction = db.Column(db.String(255), nullable=False)  # 横向，纵向 +
    Print_Colour = db.Column(db.String(255), nullable=False)   # +
    Print_size = db.Column(db.String(255), nullable=False)
    Print_way = db.Column(db.String(255), nullable=False)  # 打印的方式，单面或双面
    Print_Money = db.Column(db.Float())  # 订单价格
    Print_Status = db.Column(db.Integer(), default=0)  # 订单状态，0:已提交文件但未支付, 1:已经支付但未打印, 2:已经加入下载队列, 3:已打印
    Trade_Number = db.Column(db.String(255))  # 支付订单号

    User_Id = db.Column(db.Integer(), db.ForeignKey('User.Id'), nullable=False)

    # user = db.relationship('User', foreign_keys='Order.User_Id')

    def to_json(self):


        tel_num = User.query.filter(User.Id == self.User_Id).first()
        # born_date = str(self.Born_Date.year) + "-" + str(self.Born_Date.month) + "-" + str(
        #     self.Born_Date.day) + " " + str(self.Born_Date.hour) + ":" + str(self.Born_Date.minute) + ":" + str(
        #     self.Born_Date.second)
        if self.Print_way == 'one-sided':
            print_way = '单面'
        elif self.Print_way == 'two-sided-long-edge':
            print_way = '双面长边'
        else:
            print_way = '双面短边'
        if self.Print_Status == 0:
            status = '未支付'
        elif self.Print_Status == 1:
            status = '已支付'
        elif self.Print_Status == 2:
            status = '正在打印'
        else:
            status = '打印完成'
        if self.Print_Colour == 'CMYGray':
            color = '黑白'
        else:
            color = '彩色'

        if self.Time_Way == 0:
            file_dir = "<div><a href='../../static/Upload_Files/BeforeSwitchFile/"+ self.File_Dir +"' target='_blank' class='layui-table-link'>"+ self.File_Name +"</a></div>"
        else:
            if self.File_Dir[-3:] == 'pdf':
                file_dir = "<div><a href='#' onclick=\"window.open('look_pdf/viewer.html?file=/static/Upload_Files/" + self.File_Dir + "','PDF','width:50%;height:50%;top:100;left:100;');\"' class='layui-table-link'>" + self.File_Name + "</a></div>"
            else:
                file_dir = "<div><a href='look_picture/" + self.File_Dir + "' target='_blank' class='layui-table-link'>" + self.File_Name + "</a></div>"
        return {
            'Print_File_Dir': file_dir,
            'Print_Money': self.Print_Money,
            'File_Name': self.File_Name,
            'Print_Status': status,
            'Print_Date': self.Print_Date,
            'Print_Copies': self.Print_Copies,
            'Print_Colour': color,
            'Print_size': self.Print_size,
            'Print_way': print_way,
            'Print_Direction':self.Print_Direction,
            'Born_Date_Day': self.Born_Date_Day,
            'Trade_Number': self.Trade_Number,
            'Tel_Num': tel_num.Tel_Number
        }

    @staticmethod
    def query_all(date, page=1):
        #activites = Order.query.filter_by(Born_Date_Day=date).all()
        activites = Order.query
        if date != '':
            activites = activites.filter(Order.Born_Date_Day == date)
            return activites.paginate(
                page, per_page=current_app.config['POST_PER_PAGE']
            )
