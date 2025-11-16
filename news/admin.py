# news/admin.py
from django.contrib import admin
from .models import Category, News, Vote
from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'get_vote_sum',  'image')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(vote_sum=Coalesce(Sum('votes__value'), Value(0)))

    def get_vote_sum(self, obj):
        return obj.vote_sum
    get_vote_sum.short_description = 'Rating'
    get_vote_sum.admin_order_field = 'vote_sum'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'value', 'created_at')
    list_filter = ('value', 'created_at')