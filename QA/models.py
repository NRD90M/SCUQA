from django.db import models
from datetime import datetime
# Create your models here.


class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    username = models.CharField(max_length=128, unique=True, primary_key=True)
    password = models.CharField(max_length=256)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now=True)
    nickname = models.CharField(max_length=50, blank=True)
    profession = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    per_signature = models.CharField(max_length=1024,blank=True)
    per_introduction = models.TextField(blank=True)
    uid_qid = models.ManyToManyField(to='Question', through='Question_Favorite', through_fields=('fauthor','question'))
    headshot_img = models.ImageField(upload_to='headshot_img', default='headshot_img/headshot.jpg')

def __str__(self):
        return self.username

class EmailVerifyRecord(models.Model):

    send_choices = (
        ('register','注册'),
        ('forget','找回密码')
    )

    code = models.CharField('验证码',max_length=20)
    email = models.EmailField('邮箱',max_length=50)
    send_type = models.CharField(choices=send_choices,max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

class UserMessage(models.Model):
    user = models.IntegerField('接受用户',default=0)
    message = models.CharField('消息内容',max_length=500)
    has_read = models.BooleanField('是否已读',default=False)
    massage_time = models.DateTimeField('添加时间', default=datetime.now)

class Feedback(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    user_feedback_email = models.EmailField()
    user_feedback_time = models.DateTimeField(auto_now=True)
    user_feedback = models.TextField(max_length=1024)
    admin_feedback = models.TextField(max_length=1024, blank=True)
    admin_feedback_time = models.DateTimeField(auto_now=True)

# 教务处新闻
class JwNews(models.Model):
    jw_news = models.CharField(max_length=150)
    jw_link = models.CharField(max_length=150)
    jw_content = models.CharField(max_length=1000)
    jw_post_time = models.CharField(blank=True,null=True,max_length=128)


# 学工部新闻
class XgNews(models.Model):
    Xg_news = models.CharField(max_length=150)
    Xg_link = models.CharField(max_length=150)
    Xg_content = models.CharField(max_length=1000)
    Xg_post_time = models.DateTimeField(blank=True,null=True)


# 学院新闻
class XyNews(models.Model):
    Xy_news = models.CharField(max_length=150)
    Xy_link = models.CharField(max_length=150)
    Xy_content = models.CharField(max_length=1000)
    Xy_post_time = models.CharField(blank=True,null=True,max_length=128)


#问题一级分类
class First_type(models.Model):
    #类别id
    ptid = models.IntegerField(unique=True, primary_key=True)
    #类别名
    pyname = models.CharField(max_length=50)

#问题二级分类
class Second_type(models.Model):
    #类别id
    tid = models.IntegerField(unique=True, primary_key=True)
    #类别名
    tname = models.CharField(max_length=50)
    #所属一级分类
    Ptype = models.ForeignKey(First_type, on_delete=models.CASCADE)

#问题
class Question(models.Model):
    #问题发布者
    qauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    #问题所属一级分类
    ftype = models.ForeignKey(First_type,on_delete=models.CASCADE)
    #问题所属二级分类
    stype = models.ForeignKey(Second_type,on_delete=models.CASCADE)
    #问题标题
    qtitle = models.CharField(max_length=100)
    #问题详情
    qcontent = models.TextField(max_length=500)
    #发布时间
    q_time = models.DateTimeField(auto_now_add=True)
    #问题相关图片
    q_img = models.ImageField(blank=True, null=True,upload_to='question_img')
    #问题相关附件
    q_file = models.FileField(blank=True, null=True, upload_to='question_file')

#问题的回答
class Answer(models.Model):
    adopt_choices = (
        (0, 'no'),
        (1, 'yes'),
    )
    #回答者
    aauthor = models.ForeignKey(User,on_delete=models.CASCADE)
    #回答所属问题
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    #回答详情
    acontent = models.TextField(max_length=500)
    #回答时间
    a_time = models.DateTimeField(auto_now_add=True)
    #是否采纳（目前未应用）
    adopt=models.SmallIntegerField(default=0,choices=adopt_choices)
    Ans_deal_choices = (
        ('0', '未处理'),
        ('1', '已处理')
    )
    Ans_deal_status = models.IntegerField(default=0, choices=Ans_deal_choices)

#回答的评论
class Answer_Comment(models.Model):
    #评论所属回答
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    #评论者
    cauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    #评论内容
    ccontent = models.TextField(max_length=500)
    #评论时间
    c_time = models.DateTimeField(auto_now_add=True)
    AnsComment_deal_choices = (
        ('0', '未处理'),
        ('1', '已处理')
    )
    AnsComment_deal_status = models.IntegerField(default=0, choices=AnsComment_deal_choices)

#回答的点赞
class Answer_Like(models.Model):
    #点赞所属问题
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    #点赞者
    lauthor = models.ForeignKey(User,on_delete=models.CASCADE)
    #点赞时间
    l_time = models.DateTimeField(auto_now_add=True)
    AnsLike_deal_choices = (
        ('0', '未处理'),
        ('1', '已处理')
    )
    AnsLike_deal_status = models.IntegerField(default=0, choices=AnsLike_deal_choices)

#关注问题
class Question_Favorite(models.Model):
    #关注的问题
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    #关注者
    fauthor = models.ForeignKey(User,on_delete=models.CASCADE)
    f_time = models.DateTimeField(auto_now_add=True)
    Followship_deal_choices = (
        ('0', '未处理'),
        ('1', '已处理')
    )
    Followship_deal_status = models.IntegerField(default=0, choices=Followship_deal_choices)

#关注用户
class User_Favorite(models.Model):
    #关注者
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_user")
    #被关注者
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_follower")
    uf_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    UserFollow_deal_choices = (
        ('0', '未处理'),
        ('1', '已处理')
    )
    UserFollow_deal_status = models.IntegerField(default=0, choices=UserFollow_deal_choices)

    class Meta:
        unique_together = ("user", "follower")

#问答社区
class Community(models.Model):
    #社区名
    c_name = models.CharField(max_length=50)
    #社区简介
    c_introduction = models.TextField(max_length=500, blank=True)
    #社区创建者
    c_author = models.ForeignKey(User,on_delete=models.CASCADE)
    #创建时间
    c_time = models.DateTimeField(auto_now_add=True)
    #社区头像
    c_img = models.ImageField(default='community_img/com.jpg', upload_to='community_img')

#申请加入社区
class Community_Apply(models.Model):
    agree_choices = (
        (0, '拒绝'),
        (1, '同意'),
        (2, '未处理'),
    )
    #申请的社区
    community =models.ForeignKey(Community,on_delete=models.CASCADE)
    #申请者
    ca_author = models.ForeignKey(User,on_delete=models.CASCADE)
    #处理申请
    agree = models.SmallIntegerField(choices=agree_choices,default=2)
    #申请时间
    ca_time = models.DateTimeField(auto_now_add=True)

#社区成员
class Community_Member(models.Model):
    #所属社区
    community = models.ForeignKey(Community,on_delete=models.CASCADE)
    #加入该社区的成员
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    #成员加入时间
    cm_time = models.DateTimeField(auto_now_add=True)

#社区的文件
class Community_File(models.Model):
    #所属社区
    community =models.ForeignKey(Community,on_delete=models.CASCADE)
    #文件名
    cf_name = models.CharField(max_length=20,default='')
    #文件
    cf_file = models.FileField(blank=True, null=True, upload_to='community_file')
    #文件上传者
    cf_author = models.ForeignKey(User,on_delete=models.CASCADE)
    #文件上传时间
    cf_time = models.DateTimeField(auto_now_add=True)

#社区公告
class Community_Notice(models.Model):
    #所属社区
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    #公告发布者（目前只有创建者能发布）
    cn_author = models.ForeignKey(User, on_delete=models.CASCADE)
    #公告标题
    cn_title = models.CharField(max_length=20)
    #公告详情
    cn_content = models.TextField(max_length=500)
    #公告发布时间
    cn_time = models.DateTimeField(auto_now_add=True)

#社区聊天
class Community_Chat(models.Model):
    #所属社区
    community = models.ForeignKey(Community,on_delete=models.CASCADE)
    #消息发送者
    cc_author = models.ForeignKey(User,on_delete=models.CASCADE)
    #文本消息
    cc_message = models.TextField(max_length=500)
    #图片
    cc_img = models.ImageField(blank=True, null=True, upload_to='chat_img')
    #文件
    cc_file = models.FileField(blank=True, null=True, upload_to='chat_file')
    #文件名
    cc_file_name = models.CharField(max_length=200, blank=True, null=True)
    #文件类型
    cc_file_type = models.CharField(max_length=20, blank=True, null=True)
    #语音消息
    cc_voice = models.FileField(blank=True, null=True, upload_to='chat_voice')
    #消息发送时间
    cc_time = models.DateTimeField(auto_now_add=True)


