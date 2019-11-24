from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'status', 'created_on')
    list_filter = ('status',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20


admin.site.register(Post, PostAdmin)