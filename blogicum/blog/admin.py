from django.contrib import admin

from blog.models import Post, Category, Location, Comment


admin.site.empty_value_display = 'Не задано'

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Comment)
