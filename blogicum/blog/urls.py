from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/',  views.PostCreateView.as_view(), name='create_post'),
    path('category/<slug:category_slug>/',
        views.PostCategoryListView.as_view(),
        name='category_posts'),
    path('profile/<slug:username>/', views.ProfileDetailView.as_view(), name='profile')
]
