from django import forms
from captcha.fields import CaptchaField
from . import models
from django.forms import widgets


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetForm(forms.Form):
    email = forms.CharField(required=True)  # 用户名不能为空
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})



class ModifyPwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


ftypes = models.First_type.objects.all()
FTYPE_CHOICES = []
FTYPE_CHOICES.append(['','请选择'])
for ftype in ftypes:
    FTYPE_CHOICES.append([ftype.ptid, ftype.pyname])
stypes = models.Second_type.objects.all()
STYPE_CHOICES = []
STYPE_CHOICES.append(['','请选择'])
for stype in stypes:
   STYPE_CHOICES.append([stype.tid, stype.tname])
class QuestionForm(forms.Form):
    ftype = forms.ChoiceField( widget = forms.Select(attrs={'class':'select', 'onChange':'getStypeOptions(this.value)'}),choices = FTYPE_CHOICES, label= '一级分类')
    stype = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select'}), label='二级分类',choices=STYPE_CHOICES)
    qtitle = forms.CharField(label="问题标题", max_length=100, widget=forms.TextInput(attrs={'class':'title'}))
    qcontent = forms.CharField(label="问题详情", max_length=500, widget=forms.Textarea(attrs={'class':'content'}))
    q_img = forms.ImageField(label="添加图片【可选】", required=False, widget=forms.FileInput(attrs={'class':'q_img'}))
    q_file = forms.FileField(label="添加附件【可选】", required=False, widget=forms.FileInput(attrs={'class': 'q_file'}))

#用户回答问题表单
class AnswerForm(forms.Form):
    acontent =  forms.CharField(label="", max_length=500, widget=forms.Textarea(attrs={'class':'a_content'}))


#用户发布社区公告表单
class NoticeForm(forms.Form):
    cn_title = forms.CharField(label="公告标题", max_length=15, widget=forms.TextInput(attrs={'class':'cn_name'}))
    cn_content = forms.CharField(label="公告详情", max_length=200, widget=forms.Textarea(attrs={'class':'cn_content'}))

#用户上传社区文件表单
class FileForm(forms.Form):
    cf_name = forms.CharField(label="文件名", max_length=15, widget=forms.TextInput(attrs={'class':'cf_name'}))
    cf_file = forms.FileField(label="选择文件", widget=forms.FileInput(attrs={'class': 'cf_file'}))
