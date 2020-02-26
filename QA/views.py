from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
from .models import User
from QA.utils.email_send import send_register_email
from QA.models import EmailVerifyRecord
from django.views.generic.base import View
from QA.forms import ForgetForm,ModifyPwdForm
from django.db.models.aggregates import Count
from django.db.models import Q
from django.http import JsonResponse,FileResponse
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .models import XgNews,JwNews,XyNews
from bs4 import BeautifulSoup
import requests
import re


def xg_news(request):
    latest_news=models.XgNews.objects.all().order_by('-Xg_post_time').first()
    if not latest_news:
        url = "http://xsc.scu.edu.cn/Website/XG/Home/NewsList?KHVjQpxkZeCaAHEYwJztexSG0umVXBCXDEuTqqjQ8VQ=.shtml"
        # headers = { 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
        scu_data = requests.get(url).content.decode('utf-8')
        soup1 = BeautifulSoup(scu_data, "html.parser")
        new = soup1.find_all('div', class_='news-list')
        new_list = new[0].select('a')
        for x in new_list:  # 对返回的列表进行遍历
            time = x.select('span')
            post_time = '2018-' + time[0].get_text()
            print(post_time)
            title = x.get('title')  # 取出标题，采用get_text()方法
            link = "http://xsc.scu.edu.cn" + x.get('href')  # 取出链接，采用get("href")方法
            content_data = requests.get(link).content.decode('utf-8')
            soup2 = BeautifulSoup(content_data, "html.parser")
            pre_content = soup2.find_all('div', class_='news-content')
            content = pre_content[0]
            content = str(content)#将列表内容转化为字符串
           # pattern = re.compile(r'<[^>]+>', re.S)
            #content = pattern.sub('', content)#使用正则去除html标签
            print(type(content))
            XgNews.objects.create(Xg_news=title, Xg_link=link, Xg_content=content, Xg_post_time=post_time)
            xg_news = models.XgNews.objects.all().order_by('-Xg_post_time')
            paginator = Paginator(xg_news, 10)
            page = request.GET.get('page', 1)
            currentPage = int(page)
            try:
                print(page)
                xg_news = paginator.page(page)
            except PageNotAnInteger:
                xg_news = paginator.page(1)
            except EmptyPage:
                xg_news = paginator.page(paginator.num_pages)
        return render(request, 'XgNews.html', locals())
    else:
        #url = "http://xsc.scu.edu.cn/Website/XG/Home/NewsList?KHVjQpxkZeCaAHEYwJztexSG0umVXBCXDEuTqqjQ8VQ=.shtml"
        # headers = { 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
       # scu_data = requests.get(url).content.decode('utf-8')
        #soup3 = BeautifulSoup(scu_data, "html.parser")
        #time_lists = (soup3.find_all('div', class_='date'))[0]
        #time_list=[]
       # for tlist in time_lists:
            #time_lise.append(tlist.get_text())
        #time_list.reverse()
        xg_news = models.XgNews.objects.all().order_by('-Xg_post_time')
        paginator = Paginator(xg_news, 10)
        page = request.GET.get('page', 1)
        currentPage = int(page)
        try:
            print(page)
            xg_news = paginator.page(page)
        except PageNotAnInteger:
            xg_news = paginator.page(1)
        except EmptyPage:
            xg_news = paginator.page(paginator.num_pages)
        return render(request, 'XgNews.html', locals())



def xg_news_detail(request,id):
    xg_news = models.XgNews.objects.get(id=id)
    if xg_news:
        return render(request, 'xg_news_detail.html',locals())
    else:
        return render(request,'XgNews.html', locals())


def jw_news(request):
    latest_news = models.JwNews.objects.all().order_by('-jw_post_time').first()
    if not latest_news:
        url="http://jwc.scu.edu.cn/"
        jw_data = requests.get(url).content.decode('utf-8')
        soup1 = BeautifulSoup(jw_data, "html.parser")
        jw_new = soup1.find_all('ul', class_='list-llb-s')
        jw_news_list=jw_new[0].select('a')
        for new in jw_news_list:
            titles = new.select('span')
            title = titles[0].get_text()
            post_times = new.find_all('em',class_='fr list-date-a')
            post_time = post_times[0].get_text()
            link = new.get("href")
            content_data = requests.get(link).content.decode('utf-8')
            soup2 = BeautifulSoup(content_data, "html.parser")
            pre_content = soup2.find_all('div', class_='page-content')
            content = pre_content[0]
            content = str(content)  # 将列表内容转化为字符串
            # pattern = re.compile(r'<[^>]+>', re.S)
            # content = pattern.sub('', content)#使用正则去除html标签
            print(type(content))
            JwNews.objects.create(jw_news=title,jw_link=link,jw_content=content,jw_post_time=post_time)
            jw_news = models.JwNews.objects.all().order_by('-jw_post_time')
        return render(request, 'JwNews.html', locals())
    else:
        jw_news = models.JwNews.objects.all()
        return render(request, 'JwNews.html', locals())


def jw_news_detail(request,id):
    jw_news = models.JwNews.objects.get(id=id)
    if jw_news:
        return render(request, 'jw_news_detail.html',locals())
    else:
        return render(request,'JwNews.html', locals())


def xy_news(request):
    latest_news = models.XyNews.objects.all()
    if not latest_news:
        for i in range(1,5):
            url="http://ggglxy.scu.edu.cn/index.php?c=article&a=type&tid=77&page="+str(i)
            xy_data = requests.get(url).content.decode('utf-8')
            soup1 = BeautifulSoup(xy_data, "html.parser")
            xy_new = soup1.find_all('ul', class_='zy_listul')
            xy_news_list=xy_new[0].select('a')
            for new in xy_news_list:
                title = new.get_text()
                link = "http://ggglxy.scu.edu.cn"+ new.get("href")
                content_data = requests.get(link).content.decode('utf-8')
                soup2 = BeautifulSoup(content_data, "html.parser")
                pre_content = soup2.find_all('div', class_='detail_zy_c pb30 mb30')
                content = pre_content[0]
                content = str(content)  # 将列表内容转化为字符串
                # pattern = re.compile(r'<[^>]+>', re.S)
                # content = pattern.sub('', content)#使用正则去除html标签
                print(type(content))
                post_time1 = soup2.find_all('div', class_='detail_zy_title')
                post_time2 = post_time1[0].select('p')
                post_time = post_time2[0].get_text()
                XyNews.objects.create(Xy_news=title,Xy_link=link,Xy_content=content,Xy_post_time=post_time)
        xy_news = models.XyNews.objects.all().order_by('-Xy_post_time')
        return render(request, 'XyNews.html', locals())
    else:
        xy_news = models.XyNews.objects.all()
        return render(request, 'XyNews.html', locals())


def xy_news_detail(request,id):
    xy_news = models.XyNews.objects.get(id=id)
    if xy_news:
        return render(request, 'xy_news_detail.html',locals())
    else:
        return render(request,'XyNews.html', locals())


#装饰器
def get_follow_num(func):
    def _get_follow_num(request):
         username = request.session["username"]
         userfollower = models.User_Favorite.objects.filter(follower_id=username)
         userfollower_num = userfollower.count()
         userfollowing = models.User_Favorite.objects.filter(user_id=username)
         userfollowing_num = userfollowing.count()
         return func(request, userfollowing_num, userfollower_num)
    return _get_follow_num

#注册
def register(request):
    if request.method == "POST":
        name = request.POST.get('username', '')
        password = request.POST.get('password','')
        password1 = request.POST.get('password1', '')
        email = request.POST.get('email', '')
        sex = request.POST.get('sex', '')
        if password != password1:
            massage = "两次输入的密码不一致！"
            return render(request, 'register.html', locals())
        else:
            same_name_user = models.User.objects.filter(username=name)
            if same_name_user:
                message = '该用户名已存在，请重新选择用户名！'
                return render(request, 'register.html', locals())
            same_email_user = models.User.objects.filter(email=email)
            if same_email_user:
                message = '该邮箱已被注册，请使用别的邮箱！'
                return render(request, 'register.html', locals())
            user = User()
            user.username = name
            user.password = password
            user.email = email
            user.sex = sex
            user.save()
            message = "注册成功！"
            return redirect('/login/')
    return render(request, 'register.html', locals())

#登录
def login(request):
    if request.method == 'POST':
        #user = User.objects.all()
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = models.User.objects.get(username=username)
            if user.password == password:
                request.session['is_login']= "yes"
                request.session['username'] = username
                #request.session.set_expiry(100)
               # request.session['password'] = user.password
                return redirect('/index/')
            else:
                message = "密码不正确！"
                return render(request, 'login.html',  locals())
        except:
            message = "用户名不存在！"
    return render(request, 'login.html')



#个人中心首页
@get_follow_num
def usercenter_index(request,userfollowing_num,userfollower_num):
    if not request.session.get('is_login') == 'yes':
        return redirect("/login/")
    username = request.session["username"]
    user=models.User.objects.get(username=username)
    return render(request, 'usercenter_index.html', locals())



 #修改用户信息
@get_follow_num
def userinfo_reset(request,userfollowing_num,userfollower_num):
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    headshot_img1 = user.headshot_img
    if request.method == 'POST':
        username = request.session["username"]
        users = models.User.objects.get(username=username)
        users.nickname = request.POST.get('user_nickname', '')
        users.sex = request.POST.get('sex', '')
        users.profession = request.POST.get('user_profession', '')
        users.email = request.POST.get('email', '')
        users.per_signature = request.POST.get('user_signature', '')
        users.per_introduction = request.POST.get('user_introduction', '')
        if request.FILES.get('head_img'):
            users.headshot_img = request.FILES.get('head_img')
        else:
            users.headshot_img = headshot_img1
        users.save()
        message = "修改成功！"
        user = models.User.objects.get(username=username)
        return render(request, 'usercenter_index.html', locals())
    return render(request, 'userinfo_reset.html', locals())


#我的消息
@get_follow_num
def user_message(request,userfollowing_num,userfollower_num):
    if not request.session.get('is_login') == 'yes':
        return redirect("/login/")
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    applys = models.Community_Apply.objects.filter(agree=2, community__c_author=user).order_by('-ca_time')
    answers = models.Answer.objects.filter(qid__qauthor=username, Ans_deal_status=0)
    ans_comments = models.Answer_Comment.objects.filter(answer__aauthor=username, AnsComment_deal_status=0)
    ans_likes = models.Answer_Like.objects.filter(answer__aauthor=username, AnsLike_deal_status=0)
    user_follows = models.User_Favorite.objects.filter(user=username, UserFollow_deal_status=0)
    return render(request, 'user_message.html', locals())


def message_deal(request):
    ans_id = request.GET.get('ans_id')
    ans_comment_id = request.GET.get('ans_comment_id')
    ans_like_id = request.GET.get('ans_like_id')
    user_follow_id = request.GET.get('user_follow_id')
    AnsDeal = models.Answer.objects.filter(id=ans_id).update(Ans_deal_status=1)
    AnsCommentDeal = models.Answer_Comment.objects.filter(id=ans_comment_id).update(AnsComment_deal_status=1)
    AnsLike = models.Answer_Like.objects.filter(id=ans_like_id).update(AnsLike_deal_status=1)
    UserFollow = models.User_Favorite.objects.filter(id=user_follow_id).update(UserFollow_deal_status=1)
    if AnsDeal:
        return fsuccess_response("处理成功")
    else:
        if AnsCommentDeal:
            return fsuccess_response("处理成功")
        else:
            if AnsLike:
                return fsuccess_response("处理成功")
            else:
                if UserFollow:
                    return fsuccess_response("处理成功")
                else:
                    return error_response("处理失败")


#我的提问
@get_follow_num
def my_question(request,userfollowing_num,userfollower_num):
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    question_list = models.Question.objects.filter(qauthor_id=username)
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page', 1)
    currentPage = int(page)
    try:
        print(page)
        question_list = paginator.page(page)
    except PageNotAnInteger:
        question_list = paginator.page(1)
    except EmptyPage:
        question_list = paginator.page(paginator.num_pages)
    return render(request, 'my_question.html', locals())


#我的回答
@get_follow_num
def my_answer(request,userfollowing_num,userfollower_num):
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    answer_list = models.Answer.objects.filter(aauthor_id=username)
    return render(request, 'my_answer.html', locals())

#我的反馈
@get_follow_num
def user_feedback(request,userfollowing_num,userfollower_num):
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    feedback_list = models.Feedback.objects.filter(username=username)
    if request.method =='POST':
        email = request.POST.get('email','')
        feedback = request.POST.get('feedback','')
        if email and feedback:
             AddFeedback=models.Feedback.objects.get_or_create(username_id=username,user_feedback=feedback,user_feedback_email=email,admin_feedback='')
             if AddFeedback:
                 message="提交成功，谢谢您的宝贵意见！"
                 return render(request,'user_feedback.html',locals())
             else:
                 message ="提交失败！"
                 return render(request, 'user_feedback.html'.locals())
        message = "邮件和反馈内容不能为空哦！"
        return render(request,'user_feedback.html',locals())
    return render(request, 'user_feedback.html', locals())


#我的粉丝
@get_follow_num
def my_followers(request,userfollowing_num,userfollower_num):
    username = request.session["username"]
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    #user = models.User.objects.get(username=userid)
    my_follower = models.User_Favorite.objects.filter(follower_id=username)
    return render(request, 'my_followers.html', locals())

#我关注的人
@get_follow_num
def my_followings(request,userfollowing_num,userfollower_num):
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    my_following = models.User_Favorite.objects.filter(user_id=username)
    return render(request, 'my_followings.html', locals())


#我关注的问题
@get_follow_num
def my_follow_questions(request,userfollowing_num,userfollower_num):
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    follows = models.Question_Favorite.objects.filter(fauthor_id=username)
    return render(request, 'my_follow_questions.html', locals())


#修改密码
@get_follow_num
def password_modify(request,userfollowing_num,userfollower_num):
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    if request.method == 'POST':
        #uu = models.User.objects.get(username='2016141093006')
        #password = request.session.get('password', None)
        username = request.session["username"]
        user = models.User.objects.get(username=username)
        password = user.password
        original_paswd = request.POST.get('original_paswd', '')
        new_paswd1 = request.POST.get('new_paswd1', '')
        new_paswd2 = request.POST.get('new_paswd2', '')
        if original_paswd and new_paswd1 and new_paswd2:
            if original_paswd == password:
                if new_paswd1== new_paswd2:
                    user1 = User.objects.get(username=username)
                    user1.password = new_paswd1
                    user1.save()
                   # message = "修改成功！"
                    return render(request, 'usercenter_index.html', locals())
                else:
                    message = "两次输入的密码不一致！"
                    return render(request, 'password_modify.html', locals())
            else:
                message = "原始密码错误！"
                return render(request, 'password_modify.html', locals())
        else:
            message="密码输入不能为空！"
            return render(request, 'password_modify.html', locals())
    return render(request, 'password_modify.html', locals())


#忘记密码(填写表单页面)
def password_forget(request):
    return render(request, 'password_forget.html')


#忘记密码（发送重置密码邮件）
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'password_forget.html', {'forget_form':forget_form })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            send_register_email(email, 'forget')
            return render(request, 'email_send_success.html')
        else:
            return render(request,'password_forget.html', {'forget_form': forget_form})

 #忘记密码（重置密码）
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "password_forget.html")
        return render(request, "password_forget.html")

#忘记密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致！"})
            user = User.objects.get(email=email)
            user.password = pwd2
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form })

#邮件发送消息提示
def send_success(request):
    return render(request, 'email_send_success.html')


#用户的提问
def user_question(req,userid):
    if req.session.get('is_login') == 'yes':
        username = req.session["username"]
        user_fav = models.User_Favorite.objects.filter(user_id=username,follower_id=userid)
    user = models.User.objects.get(username=userid)
    questions = models.Question.objects.filter(qauthor_id=userid)
    return render(req,'user_question.html',locals())

#用户的回答
def user_answer(req,userid):
    if req.session.get('is_login') == 'yes':
        username = req.session["username"]
        user_fav = models.User_Favorite.objects.filter(user_id=username,follower_id=userid)
    user = models.User.objects.get(username=userid)
    answers = models.Answer.objects.filter(aauthor_id=userid)
    return render(req,'user_answer.html',locals())

#用户关注的问题
def user_favorite(req,userid):
    if req.session.get('is_login') == 'yes':
        username = req.session["username"]
        user_fav = models.User_Favorite.objects.filter(user_id=username,follower_id=userid)
    user = models.User.objects.get(username=userid)
    favorites = models.Question_Favorite.objects.filter(fauthor_id=userid)
    return render(req, 'user_favorite.html', locals())

#用户关注的人
def user_favorite_person(req,userid):
    if req.session.get('is_login') == 'yes':
        username = req.session["username"]
        user_fav = models.User_Favorite.objects.filter(user_id=username,follower_id=userid)
    user = models.User.objects.get(username=userid)
    persons = models.User_Favorite.objects.filter(user_id=userid)
    return render(req,'user_favorite_person.html',locals())

#用户的关注者
def user_follower(req,userid):
    if req.session.get('is_login') == 'yes':
        username = req.session["username"]
        user_fav = models.User_Favorite.objects.filter(user_id=username,follower_id=userid)
    user = models.User.objects.get(username=userid)
    followers = models.User_Favorite.objects.filter(follower_id=userid)
    return render(req,'user_follower.html',locals())

#YCY



#首页
def index(req):
    xgnews = models.XgNews.objects.all().order_by("-Xg_post_time")[:5]
    recquestions = models.Question.objects.annotate(num_answers=Count('answer')).filter(num_answers__gte=1).order_by('-num_answers')[:5]
    return render(req,'index.html',locals())

#退出登录
def logout(req):
    if not req.session.get('is_login',None):
        return redirect("/index/")
    req.session.flush()
    return redirect("/index/")

def stype_list(request):
    stype_list = []
    Ptype = request.GET.get('Ptype')
    stypes = models.Second_type.objects.filter(Ptype=Ptype)
    for stype in stypes:
        c = {}
        c['name'] = stype.tname
        c['id'] = stype.tid
        stype_list.append(c)
    result = json.dumps(stype_list)
    print(result)
    return HttpResponse(result, "application/json")

#发布问题
def question(req):
    if not req.session.get('is_login') == 'yes':
        return redirect("/login/")
    if req.method == 'POST':
        que = forms.QuestionForm(req.POST,req.FILES)
        if que.is_valid():
            username = req.session["username"]
            user=models.User.objects.get(username=username)
            ftype = que.cleaned_data['ftype']
            stype = que.cleaned_data['stype']
            qtitle = que.cleaned_data['qtitle']
            qcontent = que.cleaned_data['qcontent']
            q_img = que.cleaned_data['q_img']
            q_file = que.cleaned_data['q_file']
            questionAdd=models.Question.objects.get_or_create(qauthor=user,ftype_id=ftype,stype_id=stype,qtitle=qtitle,qcontent=qcontent,q_img=q_img,q_file=q_file)
            if questionAdd:
                return redirect('/qsuccess/')
    que = forms.QuestionForm()
    return render(req,'question.html', {'que': que})

#问题发布成功
def qsuccess(req):
    username = req.session["username"]
    user = models.User.objects.get(username=username)
    questions = models.Question.objects.filter(qauthor=user).order_by('-q_time')[:1]
    question_list=[]
    for question in questions:
        stype=question.stype_id
        question_list = models.Question.objects.filter(stype_id=stype).exclude(qauthor=user)
    return render(req,'qsuccess.html',locals())

#问题的全部分类
def type_all(req):
    ftypes = models.First_type.objects.all()
    questions = models.Question.objects.all().order_by('-q_time')
    paginator = Paginator(questions, 10)
    page = req.GET.get('page', 1)
    currentPage = int(page)
    try:
        print(page)
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(req,'type_all.html',locals())

#问题的一级分类
def type1(req,ftypestid):
    ftype = models.First_type.objects.get(ptid=ftypestid)
    stypes = models.Second_type.objects.filter(Ptype_id=ftypestid)
    questions = models.Question.objects.filter(ftype_id=ftypestid).order_by('-q_time')
    paginator = Paginator(questions, 10)
    page = req.GET.get('page', 1)
    currentPage = int(page)
    try:
        print(page)
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(req, 'type1.html', locals())

#问题的二级分类
def type2(req,stypestid):
    stype=models.Second_type.objects.get(tid=stypestid)
    ftype=stype.Ptype
    questions = models.Question.objects.filter(stype_id=stypestid).order_by('-q_time')
    paginator = Paginator(questions, 10)
    page = req.GET.get('page', 1)
    currentPage = int(page)
    try:
        print(page)
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(req,'type2.html',locals())

#问题详情
def detail1(req,questionsid):
    question = models.Question.objects.get(id=questionsid)
    answers = models.Answer.objects.filter(qid_id=questionsid).order_by('-a_time')
    comments = models.Answer_Comment.objects.all().order_by('-c_time')
    if req.session.get('is_login') == 'yes':
        username = req.session["username"]
        que_fav = models.Question_Favorite.objects.filter(question_id=questionsid,fauthor_id=username)
    if req.method == 'POST':
        if not req.session.get('is_login') == 'yes':
            return redirect("/login/")
        an = forms.AnswerForm(req.POST)
        username = req.session["username"]
        user = models.User.objects.get(username=username)
        if an.is_valid():
            acontent = an.cleaned_data['acontent']
            answerAdd = models.Answer.objects.get_or_create(aauthor=user, qid=question, acontent=acontent)
            if answerAdd:
                return HttpResponseRedirect(reverse('detail1', kwargs={'questionsid': question.id}))
    else:
        an = forms.AnswerForm()
        return render(req, 'detail1.html',locals())

#评论回答
def answer_comment(req):
    if req.method == 'POST':
        if not req.session.get('is_login') == 'yes':
            return redirect("/login/")
        username = req.session["username"]
        user = models.User.objects.get(username=username)
        answer_id = req.POST.get('hidden','')
        answer = models.Answer.objects.get(id=answer_id)
        ccontent = req.POST.get('ccontent', '')
        commentAdd = models.Answer_Comment.objects.get_or_create(ccontent=ccontent, cauthor=user, answer_id=answer_id)
        if commentAdd:
            return HttpResponseRedirect(reverse('detail1',kwargs={'questionsid':answer.qid_id}))
    return HttpResponseRedirect(reverse('detail1', kwargs={'questionsid': answer.qid_id}))

#操作成功返回点赞数量的数据
def success_response(alike):
    data = {}
    data['status'] = 'SUCCESS'
    data['alike'] = alike
    return JsonResponse(data)

#操作失败返回信息
def error_response(message):
    data = {}
    data['status'] = 'ERROR'
    data['message'] = message
    return JsonResponse(data)

def question_delete(request):
    question_id = request.GET.get('question_id')
    if models.Question.objects.filter(id=question_id).exists():
        models.Question.objects.get(id=question_id).delete()
        return fsuccess_response("删除成功")
    else:
        return error_response('删除失败')

def answer_delete(request):
    answer_id = request.GET.get('answer_id')
    answer = models.Answer.objects.get(id=answer_id)
    if answer:
        models.Answer.objects.get(id=answer_id).delete()
        return fsuccess_response("删除成功")
    else:
        return error_response('删除失败')

#改变问题回答的点赞状态
def like_change(request):
    if not request.session.get('is_login') == 'yes':
        return error_response('未登录，不能进行点赞操作')
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    answer_id = request.GET.get('answer_id')
    answer = models.Answer.objects.get(id=answer_id)
    is_like = request.GET.get('is_like')
    if is_like == 'true':
        an_like = models.Answer_Like.objects.filter(answer_id=answer_id,lauthor=user)
        if not an_like:
            models.Answer_Like.objects.create(answer_id=answer_id, lauthor=user)
            alike = answer.answer_like_set.count()
            return success_response(alike)
        else:
            return error_response('已经点赞过')
    else:
        if models.Answer_Like.objects.filter(answer_id=answer_id,lauthor=user).exists():
            models.Answer_Like.objects.get(answer_id=answer_id,lauthor=user).delete()
            alike = answer.answer_like_set.count()
            return success_response(alike)
        else:
            return error_response('数据不存在，不能取消点赞')

#操作成功返回信息
def fsuccess_response(message):
    data = {}
    data['status'] = 'SUCCESS'
    data['message'] = message
    return JsonResponse(data)

#改变问题被关注的状态
def fav_change(request):
    if not request.session.get('is_login') == 'yes':
        return error_response('未登录，不能进行关注操作')
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    question_id = request.GET.get('question_id')
    is_fav = request.GET.get('is_fav')

    if is_fav == 'true':
        q_fav = models.Question_Favorite.objects.filter(question_id=question_id, fauthor=user)
        if not q_fav:
            models.Question_Favorite.objects.create(question_id=question_id, fauthor=user)
            return fsuccess_response("关注成功")
        else:
            # 已经进行过点赞
            return error_response('已经关注过')
    else:
        if models.Question_Favorite.objects.filter(question_id=question_id, fauthor=user).exists():
            models.Question_Favorite.objects.get(question_id=question_id, fauthor=user).delete()
            return fsuccess_response("取消关注成功")
        else:
            # 数据不存在，不能取消点赞
            return error_response('数据不存在，不能取消关注')

#改变用户被关注的状态
def user_fav_change(request):
    if not request.session.get('is_login') == 'yes':
        return error_response('未登录，不能进行关注操作')
    username = request.session["username"]
    user = models.User.objects.get(username=username)
    user_id = request.GET.get('user_id')
    is_fav = request.GET.get('is_fav')

    if is_fav == 'true':
        q_fav = models.User_Favorite.objects.filter(user=user, follower_id=user_id)
        if not q_fav:
            models.User_Favorite.objects.create(user=user, follower_id=user_id)
            return fsuccess_response("关注成功")
        else:
            # 已经进行过点赞
            return error_response('已经关注过')
    else:
        if models.User_Favorite.objects.filter(user=user, follower_id=user_id).exists():
            models.User_Favorite.objects.get(user=user, follower_id=user_id).delete()
            return fsuccess_response("取消关注成功")
        else:
            # 数据不存在，不能取消点赞
            return error_response('数据不存在，不能取消关注')

#热门问题
def hot_question(req):
    questions = models.Question.objects.annotate(num_answers=Count('answer')).filter(num_answers__gte=1).order_by('-num_answers')
    return render(req,'hot_question.html',locals())

#热门回答
def hot_answer(req):
    question_list=[]
    answers = models.Answer.objects.annotate(num_comments=Count('answer_comment')).filter(num_comments__gte=1).order_by('-num_comments')
    for answer in answers:
        question=answer.qid
        if question not in question_list:
            question_list.append(question)
    return render(req,'hot_answer.html',locals())

#热门回答者
def hot_answerer(req):
    users = models.User.objects.annotate(num_answers=Count('answer')).filter(num_answers__gte=2).order_by('-num_answers')
    return render(req,'hot_answerer.html',locals())

#可能感兴趣的问题推荐
def recommend_question(req):
    if not req.session.get('is_login') == 'yes':
        return redirect("/login/")
    username = req.session["username"]
    user = models.User.objects.get(username=username)
    aquestions = models.Question.objects.filter(qauthor=user)
    question_list=[]
    for aquestion in aquestions:
        stype = aquestion.stype_id
        questions = models.Question.objects.filter(stype_id=stype).exclude(qauthor=user).order_by('-q_time')
        for question in questions:
            if question not in question_list:
                question_list.append(question)
    return render(req,'recommend_question.html',locals())

#可能感兴趣的用户推荐
def recommend_user(req):
    if not req.session.get('is_login') == 'yes':
        return redirect("/login/")
    username = req.session["username"]
    user = models.User.objects.get(username=username)
    aquestions = models.Question.objects.filter(qauthor=user)
    user_list=[]
    for aquestion in aquestions:
        stype = aquestion.stype_id
        questions = models.Question.objects.filter(stype_id=stype).exclude(qauthor=user)
        for question in questions:
            user=question.qauthor
            if user not in user_list:
                user_list.append(user)
    return render(req,'recommend_user.html',locals())

#问答社区列表
def community_list(req):
    community_list = models.Community.objects.all().order_by('-c_time')
    paginator = Paginator(community_list, 5)
    page = req.GET.get('page', 1)
    currentPage = int(page)
    try:
        print(page)
        community_list = paginator.page(page)
    except PageNotAnInteger:
        community_list = paginator.page(1)
    except EmptyPage:
        community_list = paginator.page(paginator.num_pages)
    return render(req,'community_list.html',locals())

#申请加入问答社区
def community_apply(req):
    if not req.session.get('is_login') == 'yes':
        return error_response('未登录，不能进行关注操作')
    username = req.session["username"]
    user = models.User.objects.get(username=username)
    community_id = req.GET.get('community_id')
    is_apply = req.GET.get('is_apply')
    if is_apply == 'true':
        q_fav = models.Community_Apply.objects.filter(community_id=community_id, ca_author=user)
        if not q_fav:
            models.Community_Apply.objects.create(community_id=community_id, ca_author=user)
            return fsuccess_response("申请成功")
        else:
            return error_response("请勿重复申请")

#社区模糊查询（社区名和简介）
def community_search(req):
    if req.method == 'POST':
        c_word = req.POST.get('c_word', '')
        community_list = models.Community.objects.filter(Q(c_name__icontains=c_word) | Q(c_introduction__icontains=c_word)).order_by('-c_time')
    return render(req,'community_search.html',locals())

#用户创建社区
def community_create(req):
    if not req.session.get('is_login') == 'yes':
        return redirect("/login/")
    if req.method == 'POST':
        username = req.session["username"]
        user=models.User.objects.get(username=username)
        c_name = req.POST['c_name']
        if not c_name:
            return error_response('社区名称必填')
        c_introduction = req.POST['c_introduction']
        c_img = req.FILES['c_img']
        communityAdd = models.Community.objects.get_or_create(c_name=c_name,c_introduction=c_introduction,c_author=user,c_img=c_img)
        if communityAdd:
            return fsuccess_response('创建成功')
        else:
            return error_response('创建失败')
    return render(req, 'community_create.html')

#社区详情（信息介绍、公告和成员）
def community_detail(req,id):
    community = models.Community.objects.get(id=id)
    notices = models.Community_Notice.objects.filter(community=community).order_by('-cn_time')
    members = models.Community_Member.objects.filter(community=community)
    return render(req,'community_detail.html',locals())

#社区文件展示及下载
def community_file(req,id):
    community = models.Community.objects.get(id=id)
    files = models.Community_File.objects.filter(community=community).order_by('-cf_time')
    fil = forms.FileForm()
    return render(req,'community_file.html',locals())

#社区聊天界面
def community_chat(req,id):
    community = models.Community.objects.get(id=id)
    if req.method == 'POST':
        username = req.session["username"]
        user = models.User.objects.get(username=username)
        cc_message = req.POST.get('cc_message','')
        cc_file_name = req.POST.get('file_name','')
        cc_file_type = req.POST.get('file_type','')
        cc_img = req.FILES.get('cc_img','')
        cc_file = req.FILES.get('cc_file', '')
        message = cc_message.replace("\r","")
        message = message.replace("\n","")
        message = message.replace("\u00a0","")
        if message or cc_img or cc_file:
            models.Community_Chat.objects.create(cc_file_type=cc_file_type, cc_file_name=cc_file_name, cc_message=cc_message, cc_img=cc_img,cc_file=cc_file,cc_author=user, community=community)
            return fsuccess_response("")
        else:
            return error_response('消息不可为空')
    return render(req,'community_chat.html',locals())

#社区聊天语音信息发送
def chat_voice(req):
    if req.method == 'POST':
        username = req.session["username"]
        user = models.User.objects.get(username=username)
        community_id = req.POST.get('community_id', '')
        community = models.Community.objects.get(id=community_id)
        cc_voice = req.FILES['cc_voice']
        if cc_voice:
            models.Community_Chat.objects.create(cc_voice=cc_voice, cc_author=user,community=community)
            return fsuccess_response("发送成功")
        else:
            return error_response("发送失败")

#获取社区聊天信息
def chat_message(req):
    chat_list = []
    id = req.GET.get('id')
    last_chat_id = req.GET.get('last_chat_id')
    community = models.Community.objects.get(id=id)
    chats = models.Community_Chat.objects.filter(community=community,id__gt=last_chat_id)
    for chat in chats:
        c = {}
        c['id'] = chat.id
        c['cc_author'] = chat.cc_author.username
        c['cc_message'] = chat.cc_message
        c['cc_file_name'] = chat.cc_file_name
        c['cc_file_type'] = chat.cc_file_type
        c['cc_img'] = str(chat.cc_img)
        c['cc_file'] = str(chat.cc_file)
        c['cc_voice'] = str(chat.cc_voice)
        chat_list.append(c)
    result = json.dumps(chat_list)
    print(result)
    return  HttpResponse(result, "application/json")

#社区聊天文件下载
def file_download(request,chatid):
    Cfile = models.Community_Chat.objects.get(id=chatid)
    path = Cfile.cc_file
    path='media/'+str(path)
    file=open(path,'rb')
    name = Cfile.cc_file_name
    name = 'attachment;filename='+name
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']=name.encode('utf-8', 'ISO-8859-1')
    return response

#社区创建者发布公告
def community_notice(req,id):
    if not req.session.get('is_login') == 'yes':
        return redirect("/login/")
    community = models.Community.objects.get(id=id)
    if req.method == 'POST':
        noti = forms.NoticeForm(req.POST)
        if noti.is_valid():
            username = req.session["username"]
            user=models.User.objects.get(username=username)
            cn_title = noti.cleaned_data['cn_title']
            cn_content = noti.cleaned_data['cn_content']
            noticeAdd = models.Community_Notice.objects.get_or_create(cn_title=cn_title,cn_content=cn_content,cn_author=user,community=community)
            if noticeAdd:
                return HttpResponseRedirect(reverse('community_detail',kwargs={'id':community.id}))
    noti = forms.NoticeForm()
    return render(req,'community_notice.html',{'noti':noti})

#社区文件上传
def upload_file(req):
    if not req.session.get('is_login') == 'yes':
        return redirect("/login/")
    if req.method == 'POST':
         fil= forms.FileForm(req.POST,req.FILES)
         if fil.is_valid():
            username = req.session["username"]
            user = models.User.objects.get(username=username)
            community_id = req.POST.get('hidden','')
            cf_name = fil.cleaned_data['cf_name']
            cf_file= fil.cleaned_data['cf_file']
            fileAdd = models.Community_File.objects.get_or_create(cf_author=user,community_id=community_id,cf_file=cf_file,cf_name=cf_name)
            if fileAdd:
                return HttpResponseRedirect(reverse('community_file',kwargs={'id':community_id}))
    return HttpResponseRedirect(reverse('community_file', kwargs={'id': community_id}))

#信息界面（仅含用户申请加入社区的信息）


#处理用户申请加入社区信息
def apply_agree(req):
    community_id = req.GET.get('community_id')
    ca_author_id = req.GET.get('ca_author_id')
    agree = req.GET.get('agree')
    if agree == 'true':
        applyAdd = models.Community_Apply.objects.filter(community_id=community_id,ca_author_id=ca_author_id).update(agree=1)
        memberAdd = models.Community_Member.objects.get_or_create(community_id=community_id,member_id=ca_author_id)
        if applyAdd and memberAdd:
            return fsuccess_response("处理成功")
    else:
        applyAdd = models.Community_Apply.objects.filter(community_id=community_id,ca_author_id=ca_author_id).update(agree=0)
        if applyAdd:
            return fsuccess_response("处理成功")
    return error_response("处理失败")
