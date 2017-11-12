# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import transaction
import datetime
from itertools import chain
from operator import attrgetter
from grumblr.models import *
from grumblr.forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404, HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string


@login_required
def home(request):
	all_items = Item.objects.all().order_by('-item_time')
	return render(request, 'grumblr/global.html', {'items' : all_items})

@login_required
def followinghome(request):
	return render(request, 'grumblr/following.html')

@login_required
def get_following(request):
	items = Item.objects.none()
	user = request.user
	following_profile = user.profile.followed_by.all()
	print(following_profile)
	for f in following_profile:
		f_user = f.user
		f_items = Item.objects.filter(user = f_user)
		items = sorted(chain(items, f_items),key=attrgetter('item_time'), reverse=True)
	for item in items:
		cmt_btn = "cmt-btn-%d" % item.id
		cmt_field = "comment-field-%d" % item.id
		cmt_list = "comment-list-%d" % item.id
		item.html = render_to_string('grumblr/item.html', {"item": item,
														   "cmt_btn": cmt_btn, 
														   "cmt_field": cmt_field,
														   "cmt_list": cmt_list})


	context = {"items": items}

	return render(request, 'grumblr/following.json', context, content_type = 'application/json')

	


@login_required
def profile(request, user_id):
	try:
		user = User.objects.get(id = user_id)
		if user == request.user:
			flag = "0"
		else:
			me = request.user
			try:
				go = me.profile.followed_by.get(user=user)
			except ObjectDoesNotExist:
				go = None

			if go==None:
				flag = "1" #I can unfollow
			else:
				flag = "2" #I can follow
		
		items = Item.objects.filter(user=user).order_by('-item_time')
		count = Item.objects.filter(user=user).count()
		fullname = user.get_full_name()
		user.profile.save()
		user.save()
		try:
			follower=user.profile.followed.all().count()
		except ObjectDoesNotExist:
			follower=0

		try:
			following=user.profile.followed_by.all().count()
		except ObjectDoesNotExist:
			following=0

		return render(request, 'grumblr/profile.html', {'items':items, 
														'user':user,
														'fullname':fullname,
														'flag':flag,
														'follower':follower,
														'following':following,
														'count':count,
														})
	except ObjectDoesNotExist:
		return redirect('/grumblr/')

@login_required
def get_profile(request, user_id):
	try:
		user = User.objects.get(id = user_id)
	except ObjectDoesNotExist:
		return redirect('/grumblr/')
		
	items = Item.objects.filter(user=user).order_by('-item_time')

	
	for item in items:
		cmt_btn = "cmt-btn-%d" % item.id
		cmt_field = "comment-field-%d" % item.id
		cmt_list = "comment-list-%d" % item.id
		item.html = render_to_string('grumblr/item.html', {"item": item,
														   "cmt_btn": cmt_btn, 
														   "cmt_field": cmt_field,
														   "cmt_list": cmt_list})


	context = {"items": items}

	return render(request, 'grumblr/following.json', context, content_type = 'application/json')


@login_required
def edit_profile(request):
	context = {}
	if request.method == 'GET':
		context['form'] = ProfileForm()
		return render(request, 'grumblr/editprofile.html', context)

	form = ProfileForm(request.POST, request.FILES)
	context['form'] = form

	if not form.is_valid():
		print(1)
		return render(request, 'grumblr/editprofile.html', context)

	# Edit firstname and lastname
	user = request.user
	user.first_name = form.cleaned_data['firstname']
	user.last_name = form.cleaned_data['lastname']
	# Edit age/bio
	user.profile.age = form.cleaned_data['age']
	user.profile.bio = form.cleaned_data['bio']
	user.profile.image = form.cleaned_data['image']
	user.profile.save()
	user.save()

	flag = "0"

	items = Item.objects.filter(user=user).order_by('-item_time')
	count = Item.objects.filter(user=user).count()
	fullname = user.get_full_name()
	try:
		follower=user.profile.followed.all().count()
	except ObjectDoesNotExist:
		follower=0

	try:
		following=user.profile.followed_by.all().count()
	except ObjectDoesNotExist:
		following=0
	return render(request, 'grumblr/profile.html', {'items':items, 
													'user':user, 
													'fullname':fullname,
													'flag':flag,
													'follower':follower,
													'following':following,
													'count':count,
													})
@login_required
def follow(request, user_id):
	me = request.user

	try:
		others = User.objects.get(id = user_id)
	except ObjectDoesNotExist:
		raise Http404

	
	if(request.user.profile.flag == True):
		others.profile.followed.add(me.profile) #I follow others.
		others.profile.save()
		others.save()
		flag = "2"
	else:
		flag = "1"

	items = Item.objects.filter(user=others).order_by('-item_time')
	count = Item.objects.filter(user=others).count()
	fullname = others.get_full_name()
	try:
		follower=others.profile.followed.all().count()
	except ObjectDoesNotExist:
		follower=0

	try:
		following=others.profile.followed_by.all().count()
	except ObjectDoesNotExist:
		following=0
	return render(request, 'grumblr/profile.html', {'items':items, 
												'user':others, 
												'fullname':fullname,
												'flag':flag,
												'follower':follower,
												'following':following,
												'count':count,
												})



@login_required
def unfollow(request, user_id):
	me = request.user
	others = User.objects.get(id = user_id)
	others.profile.followed.remove(me.profile) #I unfollow others.
	others.profile.save()
	others.save()
	flag = "1"

	items = Item.objects.filter(user=others).order_by('-item_time')
	count = Item.objects.filter(user=others).count()
	fullname = others.get_full_name()
	try:
		follower=others.profile.followed.all().count()
	except ObjectDoesNotExist:
		follower=0

	try:
		following=others.profile.followed_by.all().count()
	except ObjectDoesNotExist:
		following=0
	return render(request, 'grumblr/profile.html', {'items':items, 
													'user':others, 
													'fullname':fullname,
													'flag':flag,
													'follower':follower,
													'following':following,
													'count':count,
													})
@login_required
def send_change_email(request):
	token = default_token_generator.make_token(request.user)
	email_body = """
	Click following link to change password:
	http://%s%s
	"""%(request.get_host(), reverse('changepassword', args=(request.user.username, token)))

	send_mail(subject="Change your password",
			  message = email_body,
			  from_email="mabel.zlou@gmail.com",
			  recipient_list=[request.user.email])
	message = "Email has been sent."
	return render(request, "grumblr/email.html", {'message':message})

@login_required
def send_confirm_email(request):
	token = default_token_generator.make_token(request.user)
	email_body = """
	Click following link to confirm:
	http://%s%s
	"""%(request.get_host(), reverse('confirm', args=(request.user.username, token)))

	send_mail(subject="Confirm your registration",
			  message = email_body,
			  from_email="mabel.zlou@gmail.com",
			  recipient_list=[request.user.email])
	message = "Email has been sent."
	return render(request, "grumblr/email.html", {'message':message})

@transaction.atomic
def confirm(request, username, token):
	context = {}
	try:
		user = User.objects.get(username=username)
	except ObjectDoesNotExist:
		raise Http404

	if not default_token_generator.check_token(user, token):
		raise Http404

	user.profile.flag = True
	user.profile.save()
	user.save()
	login(request, user)
	return redirect('/grumblr/')


@transaction.atomic
def change_password(request, username, token):
	context = {}
	try:
		user = User.objects.get(username=username)
	except ObjectDoesNotExist:
		raise Http404

	if not default_token_generator.check_token(user, token):
		raise Http404

	if request.method == 'GET':
		context['form'] = ChangePasswordForm()
		return render(request, 'grumblr/changepassword.html', context)

	form = ChangePasswordForm(request.POST)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'grumblr/changepassword.html', context)
	user.set_password(form.cleaned_data['password1'])  
	user.save()
	message = "Your password has been changed."
	login(request, user)
	return render(request, "grumblr/email.html", {'message':message})

@login_required
def add_item(request):
	if not 'item' in request.POST or not request.POST['item']:
		raise Http404
	else:
		if(request.user.profile.flag == False):
			return redirect("/grumblr/")
		else:
			new_item = Item(item_content=request.POST['item'], 
							user=request.user,
							item_time=datetime.datetime.now())
			new_item.save()

	return HttpResponse("")

@login_required
def add_comment(request, item_id):
	try:
		item = Item.objects.get(id = item_id)
	except ObjectDoesNotExist:
		raise Http404

	if not 'comment' in request.POST or not request.POST['comment']:
		raise Http404
	else:
		if(request.user.profile.flag == True):
			new_comment = Comment(item=item,
								  user=request.user,
								  comment_time=datetime.datetime.now(),
								  comment_content=request.POST['comment'])
			new_comment.save()

	return HttpResponse("")

@login_required
def get_comment(request, item_id):
	print("getting comment from" + item_id)
	this_item = Item.objects.get(id = item_id)
	comments = Comment.objects.filter(item=this_item).order_by("-comment_time")
	for comment in comments:
		comment.html = render_to_string('grumblr/comment.html', {"comment": comment})
	context = {"comments": comments, "item_id": item_id}
	return render(request, 'grumblr/comments.json', context, content_type = 'application/json')


@transaction.atomic
def register(request):
	context = {}

	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'grumblr/registration.html', context)

	form = RegistrationForm(request.POST)
	context['form'] = form

	#checks the validity of the form data
	if not form.is_valid():
		return render(request, 'grumblr/registration.html', context)

	new_user = User.objects.create_user(username = form.cleaned_data['username'],
										password = request.POST['password1'],
										first_name = form.cleaned_data['firstname'],
										last_name = form.cleaned_data['lastname'],
										email = form.cleaned_data['email'])
	new_profile = Profile(user = new_user)
	new_profile.save()
	new_user.save()

	

	new_user = authenticate(username=request.POST['username'],
							password=request.POST['password1'])

	login(request, new_user)
	token = default_token_generator.make_token(new_user)
	email_body = """
	Click following link to confirm:
	http://%s%s
	"""%(request.get_host(), reverse('confirm', args=(new_user.username, token)))

	send_mail(subject="Confirm your registration",
			  message = email_body,
			  from_email="mabel.zlou@gmail.com",
			  recipient_list=[new_user.email])
	return redirect('/grumblr/')


@login_required
def get_changes(request, time="1970-01-01T00:00+00:00"):
	max_time = Item.get_max_time()
	items = Item.get_changes(time)
	for item in items:
		cmt_btn = "cmt-btn-%d" % item.id
		cmt_field = "comment-field-%d" % item.id
		cmt_list = "comment-list-%d" % item.id
		item.html = render_to_string('grumblr/item.html', {"item": item,
														   "cmt_btn": cmt_btn, 
														   "cmt_field": cmt_field,
														   "cmt_list": cmt_list})

	context = {"max_time":max_time, "items": items}

	return render(request, 'grumblr/items.json', context, content_type = 'application/json')
