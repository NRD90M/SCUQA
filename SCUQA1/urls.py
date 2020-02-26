"""SCUQA1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from QA import views
from QA.views import ForgetPwdView,ModifyPwdView,ResetView


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^index/$', views.index,name='index'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^question/$', views.question, name='question'),
    url(r'^stype_list/$',views.stype_list,name='stype_list'),
    url(r'^qsuccess/$', views.qsuccess, name='qsuccess'),
    url(r'^type_all/$', views.type_all, name='type_all'),
    url(r'^type1-(?P<ftypestid>\d+)/$', views.type1, name='type1'),
    url(r'^type2-(?P<stypestid>\d+)/$', views.type2, name='type2'),
    url(r'^detail-(?P<questionsid>\d+)/$', views.detail1, name='detail1'),
    url(r'^question_delete/$', views.question_delete, name='question_delete'),
    url(r'^answer_delete/$', views.answer_delete, name='answer_delete'),
    url(r'^answer_comment/$', views.answer_comment, name='answer_comment'),
    url(r'^like_change/$', views.like_change, name='like_change'),
    url(r'^fav_change/$', views.fav_change, name='fav_change'),
    url(r'^user_fav_change/$', views.user_fav_change, name='user_fav_change'),
    url(r'^recommend_hot_question/$', views.hot_question,name='hot_question'),
    url(r'^recommend_hot_answer/$', views.hot_answer, name='hot_answer'),
    url(r'^recommend_hot_answerer/$', views.hot_answerer, name='hot_answerer'),
    url(r'^recommend_question/$', views.recommend_question,name='recommend_question'),
    url(r'^recommend_user/$', views.recommend_user,name='recommend_user'),
    url(r'^user-(?P<userid>\d+)/user_question/$', views.user_question, name='user_question'),
    url(r'^user-(?P<userid>\d+)/user_answer/$', views.user_answer, name='user_answer'),
    url(r'^user-(?P<userid>\d+)/user_favorite/$', views.user_favorite, name='user_favorite'),
    url(r'^user-(?P<userid>\d+)/user_favorite_person/$', views.user_favorite_person, name='user_favorite_person'),
    url(r'^user-(?P<userid>\d+)/user_follower/$', views.user_follower, name='user_follower'),
    url(r'^community_list/$', views.community_list, name='community_list'),
    url(r'^community_create/$', views.community_create, name='community_create'),
    url(r'^community_apply/$', views.community_apply, name='community_apply'),
    url(r'^community_search/$', views.community_search, name='community_search'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^apply_agree/$', views.apply_agree, name='apply_agree'),
    url(r'^chat_message/$', views.chat_message, name='chat_message'),
    url(r'^file_download-(?P<chatid>\d*)/$', views.file_download, name='file_download'),
    url(r'^chat_voice/$', views.chat_voice, name='chat_voice'),


    path('', views.index),
    path('admin/', admin.site.urls),
    path('register/', views.register,name='register'),
    path('login/', views.login),
    path('usercenter_index/', views.usercenter_index),
    path('user_message/', views.user_message),
    path('message_deal/', views.message_deal),
    path('userinfo_reset/', views.userinfo_reset),
    path('my_question/', views.my_question),
    path('my_answer/', views.my_answer),
    path('user_feedback/', views.user_feedback),
    path('password_forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    path('password_modify/', views.password_modify),
    path('email_send_success/', views.send_success),
    path('captcha/', include('captcha.urls')),
    path('my_followers/', views.my_followers),
    path('my_followings/', views.my_followings),
    path('my_follow_questions/', views.my_follow_questions),
    path('xg_news/', views.xg_news),
    path('jw_news/', views.jw_news),
    path('xy_news/', views.xy_news),
    url(r'^community-(?P<id>\d+)/detail/$', views.community_detail, name='community_detail'),
    url(r'^community-(?P<id>\d+)/file/$', views.community_file, name='community_file'),
    url(r'^community-(?P<id>\d+)/chat/$', views.community_chat, name='community_chat'),
    url(r'^community-(?P<id>\d+)/notice/$', views.community_notice, name='community_notice'),
    url(r'^xg-news-(?P<id>\d+)/detail/$',views.xg_news_detail),
    url(r'^jw-news-(?P<id>\d+)/detail/$',views.jw_news_detail),
    url(r'^xy-news-(?P<id>\d+)/detail/$',views.xy_news_detail),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
