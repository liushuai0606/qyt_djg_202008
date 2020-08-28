#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from django.shortcuts import render
from forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group


def djg_login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            # 设置回话变量 姓名
            request.session['fname'] = request.user.first_name
            # 如果属于employee组, 就设置 device_permission 会话变量
            if Group.objects.get(name='employee') in user.groups.all():
                request.session['device_permission'] = True
            # 如果用户有'qyt_device.view_devicedb'权限, 就设置 device_permission 会话变量
            elif 'qyt_device.view_devicedb' in request.user.get_all_permissions():
                request.session['device_permission'] = True
            # 如果客户从其它页面重定向过来的, 就让它返回原始页面
            next_url = request.GET.get('next', '/')
            return HttpResponseRedirect(next_url)

        else:
            return render(request, 'registration/login.html', {'form': form, 'error': '用户名或密码错误'})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        else:
            form = UserForm()
            return render(request, 'registration/login.html', {'form': form})


def djg_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')
