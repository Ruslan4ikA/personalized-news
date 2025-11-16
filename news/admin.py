# news/admin.py
from django.contrib import admin
from .models import Category, News, Vote
from django.db import models

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'get_total_votes',  'image')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(vote_count=models.Count('votes'))

    def get_total_votes(self, obj):
        return obj.vote_count
    get_total_votes.short_description = 'Total Votes'
    get_total_votes.admin_order_field = 'vote_count'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'value', 'created_at')
    list_filter = ('value', 'created_at')