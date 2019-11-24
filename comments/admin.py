from django.contrib import admin

from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('author', 'body')
    list_per_page = 20


admin.site.register(Comment, CommentAdmin)