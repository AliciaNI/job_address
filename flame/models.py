# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

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
