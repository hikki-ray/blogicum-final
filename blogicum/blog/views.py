from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404
from .models import Post, Category

# Create your views here.


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'location', 'category', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).reverse()[:5]

    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'location', 'category', 'author'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ),
        pk=post_id
    )
    context = {
        'post': post
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    try:
        category = Category.objects.get(slug=category_slug)
    except Exception:
        category = category_slug
        post_list = []
    else:
        if category.is_published:
            post_list = Post.objects.select_related(
                'location', 'category', 'author'
            ).filter(
                is_published=True,
                category__title=category.title,
                pub_date__lte=timezone.now()
            ).reverse()
        else:
            raise Http404(f'Категория {category.title} не для публикации')

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
