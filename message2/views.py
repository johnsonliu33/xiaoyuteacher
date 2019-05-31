# 添加message接口
import sys
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from message2.models import Message,User
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# def add_message(request):
#     mid = request.POST.get('mid', '')
#     name = request.POST.get('name', '')
#     content = request.POST.get('content', '')
#     status = request.POST.get('status', '')
#     author = request.POST.get('author', '')
#
#     if mid == '' or name == '' or content == '' or author == '':
#         return JsonResponse({'status': 10021, 'message': 'parameter error'})
#
#     result = Message.objects.filter(id=mid)
#     if result:
#         return JsonResponse({'status': 10022, 'message': 'event id already exists'})
#
#     result = Message.objects.filter(name=name)
#
#     if result:
#         return JsonResponse({'status': 10023,
#                              'message': 'event name already exists'})
#     try:
#         Message.objects.create(id=mid, name=name, content=content, auther=author)
#     except:
#         return JsonResponse({'status': 10024, 'message': "参数格式有问题"})
#
#     return JsonResponse({'status':200,'message':'add message success'})

# def index(request):
#     return render(request,"index.html")

# def index(request):
#     return HttpResponse("Hello xiaoyulaoshi!")

# 登录动作
def login_action(request):
    # if request.method == 'GET':
    #     print("geget")
    #if request.method == 'POST':
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)  # 登录
        request.session['user'] = username  # 将 session 信息记录到浏览器
        response = HttpResponseRedirect('/event_manage/')
        return response
    else:
        return render(request, 'login.html', {'error': 'username or password error!'})
    # if username == 'admin' and password == 'admin123':
    #     response = HttpResponseRedirect('/event_manage/')
    #     #response.set_cookie('user', username, 3600)  # 添加浏览器 cookie return response
    #     request.session['user'] = username  # 将 session 信息记录到浏览器
    #     return response
    # else:
    #     return render(request, 'login.html', {'error': 'username or password error!'})
    # else:
    #     return HttpResponse('login failed!')

@login_required
def event_manage(request):
    #username = request.COOKIES.get('user', '')  # 读取浏览器 cookie
    message_list = Message.objects.all()
    username = request.session.get('user', '')
    return render(request, "event_manage.html", {"user": username,"messages":message_list})

# 发布会名称搜索 @login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    message_list = Message.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username,
                                                "messages": message_list})

@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = User.objects.all()
    return render(request, "guest_manage.html", {"user": username,
                                                "guests": guest_list})

# 退出登录 @login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response

#借手机的操作
@login_required
def message_index(request, message_mid):
    message = get_object_or_404(Message, id=message_mid)
    return render(request, 'message_index.html', {'message': message})