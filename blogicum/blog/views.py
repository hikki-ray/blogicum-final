from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Post, Category
from .forms import PostForm


User = get_user_model()

class IndexListView(ListView):
    model = Post
    queryset = Post.objects.filter(
        is_published=True,
        # pub_date__lte=timezone.now()
    ).select_related('category', 'author')
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
        posts = Post.objects.filter(
            author__username=self.object.username
        ).select_related('category', 'author')
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['profile'] = self.object
        context['user'] = self.request.user
        context['page_obj'] = page_obj
        return context
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.is_published = True
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})


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
