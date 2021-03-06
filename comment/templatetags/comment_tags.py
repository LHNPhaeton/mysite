from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()

def get_comment_form(obj):
    data = {}
    content_type = ContentType.objects.get_for_model(obj)
    data['content_type'] = content_type.model
    data['object_id'] = obj.pk
    data['reply_comment_id'] = 0
    form = CommentForm(initial=data)
    return form