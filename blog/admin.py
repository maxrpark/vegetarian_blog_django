from django.contrib import admin

from .models import Author, Article, Category, Comments, Tags


class CommentItemInline(admin.TabularInline):
    model = Comments
    raw_id_fields = ['article']


class ArticleAdmin(admin.ModelAdmin):
    list_diplay = ('title', "author",)
    inlines = [CommentItemInline]
    prepopulated_fields = {'slug': ('title',), }


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tag',), }


admin.site.register(Author)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments)
admin.site.register(Tags, TagAdmin)
