from django.shortcuts import render, redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import CommentForm
from django.http import JsonResponse

def update_comment(request):
    '''current_http = request.META.get('HTTP_REFERER', reverse('home'))
    # 数据检查
    user = request.user
    if not user.is_authenticated:
        return render(request, 'blog/error.html', {'messege': '用户未登录','redirect_to':current_http})
    comment_content = request.POST.get('text','').strip()
    if comment_content=='':
        return render(request, 'blog/error.html', {'messege': '评论为空','redirect_to':current_http})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'blog/error.html', {'messege': '评论对象不存在','redirect_to':current_http})

    # 检查通过，保存数据
    comment = Comment()
    comment.user = user
    comment.comment_content = comment_content
    comment.content_object = model_obj
    comment.save()

    return redirect(current_http)'''

    current_http = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST,user=request.user)
    data = {}
    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.comment_content = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        #返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.timestamp() #strftime('%Y-%m-%d %H:%M:%S')
        data['comment_content'] = comment.comment_content
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''

        #return redirect(current_http)
    else:
        data['status'] = 'ERROR'
        data['messege'] = list(comment_form.errors.values())[0][0]
        #return render(request, 'blog/error.html', {'messege': comment_form.errors, 'redirect_to': current_http})
    return  JsonResponse(data)