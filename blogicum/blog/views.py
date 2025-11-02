from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy

from .models import Post, Category
from .forms import PostForm


User = get_user_model()

class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(
        is_published=True,
        # pub_date__lte=timezone.now()
    ).select_related('category', 'author')
    template_name = 'blog/index.html'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'


class PostUpdateView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    template_name = 'blog/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('blog:post_detail', post_id=obj.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.id})


class PostDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect('blog:post_detail', post_id=obj.id)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


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
