from django.contrib import admin
from .models import Tag, Article, Comment


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInLine]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag, admin.ModelAdmin)
