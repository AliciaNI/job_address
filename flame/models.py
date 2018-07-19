# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import signals

# Create your models here.
class UserProfile(models.Model):
    nick = models.CharField(verbose_name='昵称', max_length=30)
    password = models.CharField(verbose_name='密码', max_length=150)
    user = models.OneToOneField(User, unique=True)

    def __unicode__(self):
        return self.nick

    class Meta:
        verbose_name_plural = '用户信息'

class urltype(models.Model):
    urlname = models.CharField(verbose_name='网址类型', max_length=30)
    nick = models.CharField(verbose_name='昵称', max_length=10)

    def __unicode__(self):
        return self.nick

    class Meta:
        verbose_name_plural = '网址类型'

class position_website(models.Model):
    user = models.ForeignKey(User, verbose_name='user_id', db_index=True, default=4)
    position = models.CharField(verbose_name='职位', max_length=30, default='')
    website = models.ForeignKey(urltype, verbose_name='搜索网站')
    search_time = models.DateTimeField(verbose_name='search time', default=timezone.now)
    count = models.IntegerField(verbose_name='searched count', default=0)

    def __unicode__(self):
        return self.position, self.website

    class Meta:
        verbose_name_plural = '职位网站对照表'

