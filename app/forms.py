from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField, \
    RadioField, validators, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileAllowed, FileField, FileRequired
from app.models import User

# 登录
class LoginForm(FlaskForm):
    tel = StringField('手机账号', validators=[DataRequired(message=u'手机账号不能为空')])
    password = PasswordField('密码', validators=[DataRequired(message=u'密码不能为空')])
    remember = BooleanField('记住我')
    submit = SubmitField('登陆')


# 注册
class Register(FlaskForm):
    tel = IntegerField('手机', validators=[DataRequired(message=u'手机不能为空')])
    v_code = IntegerField('验证码', validators=[DataRequired(message=u'验证码不能为空')])
    password1 = PasswordField('密码', validators=[DataRequired(message=u'密码不能为空'), Length(3, 128),
                                                EqualTo('password2', message='两次密码不一样，请重新输入')])
    password2 = PasswordField('确认密码', validators=[DataRequired(message=u'密码不能为空')])
    submit = SubmitField('提交')

    def validate_tel(self, field):
        if User.query.filter_by(Tel_Number=field.data).first():
            raise ValidationError('手机号已经注册，请直接登录')


# 打印
class Print(FlaskForm):
    print_file = FileField('上传', validators=[FileRequired()])
    print_place = SelectField('打印点', choices=[('home', '测试-前端')])
    print_time = DateField('预约时间')
    print_copies = IntegerField('打印份数')
    print_demand = SelectField('打印需求', choices=[('0' , '需要排版'), ('1' , '直接打印')])
    print_type = SelectField('排版方向', choices=[('3', '竖版'), ('4', '横版')])
    print_size = SelectField('纸张大小', choices=[('A4', 'A4')]) #, ('A3', 'A3')
    print_way = SelectField('打印格式', choices=[('one-sided', '单面'), ('two-sided-long-edge', '双面长边（奇偶同向）'), ('two-sided-short-edge', '双面短边（奇偶相反）')])
    print_color = SelectField('彩色样式', choices=[('CMYGray', '黑白'), ('RGB', '彩色')])
    submit = SubmitField('提交')


# 打印测试
class Print1(FlaskForm):
    print_file = FileField('上传', validators=[FileRequired()])
    submit = SubmitField('提交')


# 查询
class QueryForm(FlaskForm):
    tel_number = IntegerField('手机号码')
    date_time = DateField('日期')
    submit = SubmitField('查询')


# 查寻是否已经付款成功
class QueryStatus(FileField):
    submit = SubmitField('查询')


# 找回密码
class Findpassword(FlaskForm):
    tel = IntegerField('手机', validators=[DataRequired(message=u'手机不能为空')])
    v_code = IntegerField('验证码', validators=[DataRequired(message=u'验证码不能为空')])
    password1 = PasswordField('密码', validators=[DataRequired(message=u'密码不能为空'), Length(3, 128),
                                                EqualTo('password2', message='两次密码不一样，请重新输入')])
    password2 = PasswordField('确认密码', validators=[DataRequired(message=u'密码不能为空')])
    submit = SubmitField('提交')


# 修改密码
class Change_Password(FlaskForm):
    tel_number = IntegerField('手机号码')
    old_password = PasswordField('旧密码', validators=[DataRequired(message=u'密码不能为空')])
    password1 = PasswordField('新密码', validators=[DataRequired(message=u'密码不能为空'), Length(3, 128),
                                                EqualTo('password2', message='两次密码不一样，请重新输入')])
    password2 = PasswordField('确认密码', validators=[DataRequired(message=u'密码不能为空')])
    submit = SubmitField('立即提交')