import string
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from .models import Profile
from user.forms import LoginForm, RegisterForm, ChangeNicknameForm, BindEmailForm
from django.http import JsonResponse

# Create your views here.


def user_login(request):
    '''username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(request, username=username, password=password)
    #current_http = request.META.get('HTTP_REFERER','/') #获得当前网址,'/'为默认的网址，首页
    current_http = request.META.get('HTTP_REFERER', reverse('home'))  #反向解析home获得home的网址
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect(current_http)
    else:
        # Return an 'invalid login' error message.
        return render(request,'blog/error.html',{'messege':'用户名或密码不正确'})'''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            # Redirect to a success page.
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def user_register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()

            # 登录用户
            user = authenticate(username=username, password=password)
            login(request, user)

            current_http = request.GET.get('from', reverse('home'))  # 获得之前的跳转页面地址，如果获取失败则反向解析home获得home的网址
            return redirect(current_http)
    else:
        register_form = RegisterForm()
    context = {}
    context['register_form'] = register_form
    return render(request, 'register.html', context)


def user_logout(request):
    logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context = {}
    return render(request,'user_info.html',context)


def change_nickname(request):
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '我的博客|修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = request.GET.get('from', reverse('home'))
    return render(request,'form.html',context)


def bind_email(request):
    if request.method == 'POST':
        form = BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '我的博客|绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = request.GET.get('from', reverse('home'))
    return render(request,'bind_email.html',context)

def send_verification_code(request):
    email = request.GET.get('email','')
    data = {}
    if email != '':
        verification_code = ''.join(random.sample(string.digits,6)) # 生成验证码
        request.session['bind_email_code'] = verification_code # 发送验证码
        send_mail('绑定邮箱', '验证码:%s' % verification_code, '1415893461@qq.com', [email.encode('utf-8')], fail_silently=False)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
