from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Email
from flask_wtf.file import  FileField, FileRequired, FileAllowed

#登陆，注册表单
class LoginForm(FlaskForm):
    phone = StringField('手机号', render_kw={'placeholder': '你的手机号/邮箱'}, validators=[DataRequired(message=u'请输入手机号或邮箱')])
    password = PasswordField('密码', render_kw={'placeholder': '密码'}, validators=[DataRequired(), Length(6, 24)])
    submit = SubmitField('登录', render_kw={'class': 'btn btn-login'})

class RegisterForm(FlaskForm):
    phone = StringField('手机号', render_kw={'placeholder': '输入手机号'}, validators=[DataRequired(message=u'请输入手机号')])
    password = PasswordField('密码', render_kw={'placeholder': '设置一个密码'}, validators=[DataRequired(), Length(6, 24)])
    username = StringField('昵称', render_kw={'placeholder': '给自己取一个昵称吧'}, validators=[DataRequired(message=u'请输入用户名')])
    email = StringField('E-Mail', render_kw={'placeholder': '输入邮箱'}, validators=[DataRequired(message=u'请输入邮箱')])
    submit = SubmitField('完成', render_kw={'class': 'btn btn-register'})
