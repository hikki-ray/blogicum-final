from django.contrib import admin

from blog.models import Post, Category, Location, Comment


admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'pub_date', 'category']
    list_filter = ['is_published', 'category', 'pub_date']
    search_fields = ['title', 'content']
    list_editable = ['is_published']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'is_published']
    list_editable = ['is_published']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at', 'post']
    search_fields = ['text', 'author__username']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_published']
    list_editable = ['is_published']
