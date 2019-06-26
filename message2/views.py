# 添加message接口
import sys

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from message2.models import Message,User,Devices
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import logging
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)
#添加设备接口

@csrf_exempt
@login_required
def add_device(request):
    device_id = request.POST.get('device_id', '')
    device_model = request.POST.get('device_model', '')
    device_system = request.POST.get('device_system', '')
    user = request.POST.get('user', '')
    pre_user = request.POST.get('pre_user', '')
    time = request.POST.get('time', '')
    status = request.POST.get('status', '')

    if device_id == '' or device_model == '' or device_system == '' or status == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Devices.objects.filter(device_id =device_id)
    if result:
        return JsonResponse({'status': 10022, 'message': 'device id already exists'})

    try:
        Devices.objects.create(device_id=device_id, device_model=device_model, device_system=device_system, user=user,pre_user=pre_user,time=time,status=status)
    except:
        return JsonResponse({'status': 10024, 'message': "参数格式有问题"})

    return JsonResponse({'status':200,'message':'add message success'})

@login_required
#获取设备列表
def get_device_content(request):
    device_system = request.GET.get('device_system', '')
    device_model = request.GET.get('device_model', '')

    if device_system == '' and device_model=='':
        return JsonResponse({'status':10021,'message':'parameters cannot be empty'})

    if device_system != '' and device_model =='':
        datas = []
        results = Devices.objects.filter(device_system=device_system)
        logging.info('按照device_system搜索出来的结果是{}..'.format(results))
        if results:
          for r in results:
            device = {}
            device['device_model'] = r.device_model
            device['device_system'] = r.device_system
            device['user'] = r.user
            device['pre_user'] = r.pre_user
            device['time'] = r.time
            device['status'] = r.status
            logging.info('device is {}'.format(device))
            datas.append(device)
          return JsonResponse({'status':200, 'message':'success', 'data':datas})
        else:
          return JsonResponse({'status':10022, 'message':'query result is empty'})
    if device_system == '' and device_model !='':
        datas = []
        results = Devices.objects.filter(device_model=device_model)
        if results:
          for r in results:
            device = {}
            device['device_model'] = r.device_model
            device['device_system'] = r.device_system
            device['user'] = r.user
            device['pre_user'] = r.pre_user
            device['time'] = r.time
            device['status'] = r.status
            datas.append(device)
            return JsonResponse({'status':200, 'message':'success', 'data':datas})
        else:
            return JsonResponse({'status':10022, 'message':'query result is empty'})

    if device_system != '' and device_model !='':
        datas = []
        try:
            results = Devices.objects.get(device_system=device_system,device_model=device_model)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        if results:
          for r in results:
            device = {}
            device['device_model'] = r.device_model
            device['device_system'] = r.device_system
            device['user'] = r.user
            device['pre_user'] = r.pre_user
            device['time'] = r.time
            device['status'] = r.status
            datas.append(device)
            return JsonResponse({'status':200, 'message':'success', 'data':datas})
        else:
            return JsonResponse({'status':10022, 'message':'query result is empty'})

@login_required
#借手机
def borrow_mobile(request):
    device_id = request.GET.get('device_id', '')
    if device_id == '':
        return JsonResponse({'status':10021,'message':'parameters cannot be empty'})

    result = Devices.objects.filter(device_id=device_id)
    if not result:
        return JsonResponse({'status': 10022, 'message': '没有找到这个设备'})

    result_sts = Devices.objects.get(device_id=device_id).status
    logging.info('目前的借出状态是：'.format(result_sts))
    if result_sts == '1':
        return JsonResponse({'status': 10023,
                             'message': '设备已经被借走了'})
    else:
        #现在的时间
        timestp = time.time()
        struct_time = time.strftime('%Y-%m-%d', time.localtime(timestp))
        Devices.objects.filter(device_id=device_id).update(status='1')
        Devices.objects.filter(device_id=device_id).update(time=struct_time)
        return JsonResponse({'status': 200, 'message': '借手机成功'})

@login_required
#还手机
def repay_mobile(request):
    device_id = request.GET.get('device_id', '')
    if device_id == '':
        return JsonResponse({'status':10021,'message':'parameters cannot be empty'})

    result = Devices.objects.filter(device_id=device_id)
    if not result:
        return JsonResponse({'status': 10022, 'message': '没有找到这个设备'})

    result_sts = Devices.objects.get(device_id=device_id).status
    logging.info('目前的借出状态是：'.format(result_sts))
    if result_sts == '0':
        return JsonResponse({'status': 10023,
                             'message': '设备没有被借出去啊'})
    else:
        #现在的时间
        timestp = time.time()
        struct_time = time.strftime('%Y-%m-%d', time.localtime(timestp))
        Devices.objects.filter(device_id=device_id).update(status='0')
        Devices.objects.filter(device_id=device_id).update(time=struct_time)
        return JsonResponse({'status': 200, 'message': '归还手机成功'})


# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            request.session['user'] = username  # 将 session 信息记录到浏览器
            response = HttpResponseRedirect('/device_manage/')
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error!'})
    else:
        return render(request, 'login.html', {'error': 'username or password error!'})


# 退出登录 @login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response

@login_required
def device_manage(request):
    #username = request.COOKIES.get('user', '')  # 读取浏览器 cookie
    device_list = Devices.objects.all()
    paginator = Paginator(device_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    username = request.session.get('user', '')
    return render(request, "device_manage.html", {"user": username,"devices":contacts})

# 发布会名称搜索 @login_required
def search_name(request):
    device_model = request.session.get('device_model', '')
    device_system = request.GET.get("device_system", "")
    device_list = Devices.objects.filter(device_system__contains=search_name)
    return render(request, "device_manage.html", {"devices": device_list})

@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = User.objects.all()
    return render(request, "guest_manage.html", {"user": username,
                                                "guests": guest_list})




