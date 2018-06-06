from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from comment.forms import CommentForm
from comment.models import Comment
from read_statistics.utils import read_statistics_once_read, get_seven_days_read_data, get_today_hot_blogs, \
    get_yesterday_hot_blogs, get_seven_days_hot_blogs, get_one_month_hot_blogs
from .models import Blog, BlogType  # ,ReadNum

# Create your views here.

EACH_PAGE_BLOG_NUMBER = 7

def blog_base(request,blogs_all_list):
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    paginator = Paginator(blogs_all_list, EACH_PAGE_BLOG_NUMBER)  # 每EACH_PAGE_BLOG_NUMBER篇博客分为一页
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页的页码

    # 页码范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(paginator.num_pages, current_page_num + 2)+1))
    if page_range[0] - 1 > 1:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] > 1:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获得每一类博客的数量
    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    '''
    #获取每个日期博客的数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list  # Blog.objects.all()
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blogs_count'] = Blog.objects.all().count()
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog')) #blog_types_list
    context['blog_dates'] = blog_dates_dict #Blog.objects.dates('created_time', 'month', order='DESC')
    return context

def blog_list(request):
    blogs_all_list=Blog.objects.all()
    context = {}
    context = blog_base(request,blogs_all_list)
    return render(request,'blog/blog_list.html', context)


def blog_with_type(request,blog_type_pk):
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

    context = {}
    context = blog_base(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request,'blog/blog_with_type.html', context)

def blog_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = {}
    context = blog_base(request, blogs_all_list)
    return render(request,'blog/blog_with_date.html', context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)
    context = {}
    context['blog'] = blog
    #context['user'] = request.user
    context['comments'] = comments.order_by('-comment_time')
    context['comment_count'] = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk).count()
    data = {}
    data['content_type'] = blog_content_type.model
    data['object_id'] = blog_pk
    data['reply_comment_id'] = 0
    context['comment_form'] = CommentForm(initial=data)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render(request,'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key,'true')
    return response

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_blogs = get_today_hot_blogs(blog_content_type)
    yesterday_hot_blogs = get_yesterday_hot_blogs(blog_content_type)
    seven_days_hot_blogs = get_seven_days_hot_blogs(blog_content_type)
    #设置缓存
    '''seven_days_hot_blogs = cache.get('seven_days_hot_blogs')
    if seven_days_hot_blogs is None:
        seven_days_hot_blogs = get_seven_days_hot_blogs(blog_content_type)
        cache.set('seven_days_hot_blogs',seven_days_hot_blogs,3600) #有效期为3600秒'''
    one_month_hot_blogs = get_one_month_hot_blogs(blog_content_type)
    context={}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_blogs'] = today_hot_blogs
    context['yesterday_hot_blogs'] = yesterday_hot_blogs
    context['seven_days_hot_blogs'] = seven_days_hot_blogs
    context['one_month_hot_blogs'] = one_month_hot_blogs
    return render(request,'blog/home.html',context)











