from django import template
from QA import models
register = template.Library()

def community_member(username,community):
    community_member = False
    if models.Community_Member.objects.filter(community=community,member_id=username).exists():
        community_member = True
    elif username==community.c_author_id:
        community_member = True
    return community_member
register.filter('community_member', community_member)

def message_num(username):
    message_num = 0
    if username:
        user = models.User.objects.get(username=username)
        community_apply = models.Community_Apply.objects.filter(community__c_author=user, agree=2)
        message_num = community_apply.count()
    return message_num
register.filter('message_num', message_num)
