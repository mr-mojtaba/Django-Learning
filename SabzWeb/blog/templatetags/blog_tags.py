from django import template
from ..models import Post, Comment, User
from django.db.models import Count, Max, Min
from django.utils.safestring import mark_safe

# Need to install (pip install markdown)
from markdown import markdown

# Creating an object to access the simple_tag decorator
register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish


@register.simple_tag
def most_popular_posts(count=5):
    return Post.published.annotate(
        comments_count=Count('comments')
    ).order_by('-comments_count')[:count]


@register.simple_tag
def most_reading_time():
    mrt = Post.published.aggregate(Max('reading_time'))
    return mrt['reading_time__max']


@register.simple_tag
def least_reading_time():
    lrt = Post.published.aggregate(Min('reading_time'))
    return lrt['reading_time__min']


@register.simple_tag
def most_reading_time_post():
    post = Post.published.order_by('-reading_time').first()
    if post:
        return {'name': post.title, 'link': post.get_absolute_url}
    return None


@register.simple_tag
def least_reading_time_post():
    post = Post.published.order_by('reading_time').first()
    if post:
        return {'name': post.title, 'link': post.get_absolute_url}
    return None


@register.inclusion_tag("partials/latest_posts.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts,
    }
    return context


@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))
