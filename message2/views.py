# 添加message接口
import sys
from django.http import JsonResponse
from message2.models import Message

def add_message(request):
    mid = request.POST.get('mid', '')
    name = request.POST.get('name', '')
    content = request.POST.get('content', '')
    status = request.POST.get('status', '')
    author = request.POST.get('author', '')

    if mid == '' or name == '' or content == '' or author == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Message.objects.filter(id=mid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})

    result = Message.objects.filter(name=name)

    if result:
        return JsonResponse({'status': 10023,
                             'message': 'event name already exists'})
    try:
        Message.objects.create(id=mid, name=name, content=content, auther=author)
    except:
        return JsonResponse({'status': 10024, 'message': "参数格式有问题"})

    return JsonResponse({'status':200,'message':'add message success'})


