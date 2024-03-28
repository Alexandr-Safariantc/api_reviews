from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category',)
    list_editable = ('category',)
    search_fields = ('name', 'year')
    list_filter = ('category', 'genre',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'score', 'pub_date', 'title')
    search_fields = ('author',)
    list_filter = ('author', 'score', 'title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date', 'review')
    search_fields = ('author',)
    list_filter = ('author', 'review',)


admin.site.empty_value_display = 'Значение не задано'
