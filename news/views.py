from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .models import News, Category, Vote
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

def news_list(request):
    query = request.GET.get('q')
    if not query or query.strip() == '':
        query = None
    category_id = request.GET.get('category')
    try:
        category_id = int(category_id) if category_id else None
    except ValueError:
        category_id = None

    sort = request.GET.get('sort', '-created_at')

    news_qs = News.objects.select_related('category', 'author').annotate(
        vote_sum=Coalesce(Sum('votes__value'), Value(0))
    )

    if query:
        news_qs = news_qs.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    if category_id:
        news_qs = news_qs.filter(category_id=category_id)


    if sort == 'popular':
        news_qs = news_qs.order_by('-vote_sum', '-created_at')
    elif sort == 'oldest':
        news_qs = news_qs.order_by('created_at')
    else:
        news_qs = news_qs.order_by('-created_at')

    categories = Category.objects.all()

    return render(request, 'news/list.html', {
        'news_list': news_qs,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'sort': sort,
    })


def news_detail(request, pk):
    news_item = get_object_or_404(News.objects.select_related('author', 'category'), pk=pk)
    user_vote = None
    if request.user.is_authenticated:
        user_vote = news_item.votes.filter(user=request.user).first()
    return render(request, 'news/detail.html', {
        'news': news_item,
        'user_vote': user_vote,
        'login_url': settings.LOGIN_URL,
    })

@login_required
def vote_news(request, pk, value):
    news_item = get_object_or_404(News, pk=pk)
    Vote.objects.update_or_create(
        user=request.user,
        news=news_item,
        defaults={'value': value}
    )
    return redirect('news:detail', pk=pk)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            return redirect('news:list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})