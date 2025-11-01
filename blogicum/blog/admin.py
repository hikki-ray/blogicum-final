from django.contrib import admin

from blog.models import Post, Category, Location

admin.site.empty_value_display = 'Не задано'

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Location)
