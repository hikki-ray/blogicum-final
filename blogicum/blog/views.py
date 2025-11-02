from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from .models import Post, Category


User = get_user_model()

class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10


class PostCategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return Post.objects.filter(
            category__slug=category_slug,
            is_published=True,
            pub_date__lte=timezone.now()
        ).select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        context['category'] = get_object_or_404(Category, slug=category_slug)
        return context
    

class ProfileDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author__username=self.object.username)
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['profile'] = self.object
        context['user'] = self.request.user
        context['page_obj'] = page_obj
        return context


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
