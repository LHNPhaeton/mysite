from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog
import datetime

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' %(ct.model,obj.pk)
    #if not request.COOKIES.get(key):
        #总阅读数+1
    rn, rn_create = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
    rn.read_num += 1
    rn.save()

    # 当天阅读数+1
    date = timezone.now().date()
    '''if ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,date=date).count():
        rD = ReadDetail.objects.get(content_type=ct,object_id=obj.pk,date=date)
    else:
        rD = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
    '''
    rD, rD_create = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date) #替换上面的if 判断
    rD.read_num += 1
    rD.save()
    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        rD = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = rD.aggregate(read_num_sum=Sum('read_num'))
        result['read_num_sum']
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

def get_today_hot_blogs(content_type):
    today = timezone.now().date()
    rD = ReadDetail.objects.filter(content_type=content_type,date=today) #获得今天的博客阅读信息
    return rD.order_by('-read_num')[:7] #得到的博客按read_num倒序排列，取得前7条

def get_yesterday_hot_blogs(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    rD = ReadDetail.objects.filter(content_type=content_type, date=yesterday)  # 获得今天的博客阅读信息
    return rD.order_by('-read_num')[:7]  # 得到的博客按read_num倒序排列，取得前7条

def get_seven_days_hot_blogs(content_type):
    today = timezone.now().date()
    seven_days_ago = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__gt=seven_days_ago)\
                        .values('id','title').annotate(read_num_sum=Sum('read_details__read_num'))

    return blogs.order_by('-read_num_sum')[:7]  # 得到的博客按read_num倒序排列，取得前7条

def get_one_month_hot_blogs(content_type):
    today = timezone.now().date()
    one_month_ago = today - datetime.timedelta(days=30)
    blogs = Blog.objects.filter(read_details__date__gt=one_month_ago)\
                        .values('id','title').annotate(read_num_sum=Sum('read_details__read_num'))

    return blogs.order_by('-read_num_sum')[:7]  # 得到的博客按read_num倒序排列，取得前7条