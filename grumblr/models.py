# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils.html import escape
# Create your models here.

class Item(models.Model):
	item_content = models.CharField(max_length = 40)
	user = models.ForeignKey(User, default=None)
	item_time = models.DateTimeField(auto_now = True)

	@property
	def html(self):
		return self._html

	@html.setter
	def html(self, context):
		self._html = context

	@staticmethod
	def get_changes(time="1970-01-01T00:00+00:00"):
		return Item.objects.filter(item_time__gt=time).distinct().order_by('-item_time')

	@staticmethod
	def get_max_time():
		return Item.objects.all().aggregate(Max('item_time'))['item_time__max'] or "1970-01-01T00:00+00:00"

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.IntegerField(default = 0)
	bio = models.CharField(max_length = 420, default = "")
	followable = models.IntegerField(default = 1)
	followed = models.ManyToManyField('Profile', 
									 symmetrical=False, 
									 related_name='followed_by')
	image = models.ImageField(upload_to='profile_image', default='profile_image/default.png', blank=True)
	flag = models.BooleanField(default = False)

	def __unicode__(self):
		return self.user.username

class Comment(models.Model):
	item = models.ForeignKey(Item, default=None)
	user = models.ForeignKey(User, default=None)
	comment_time = models.DateTimeField(auto_now = True)
	comment_content = models.CharField(max_length = 100)

	@property
	def html(self):
		return self._html

	@html.setter
	def html(self, context):
		self._html = context
