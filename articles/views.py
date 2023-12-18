from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from .models import Article, Tag


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'

    def get_queryset(self):
        filter_type = self.request.GET.get('filter')
        queryset = super().get_queryset()

        if filter_type == 'new':
            queryset = queryset.order_by('-date')[:10]  # Fetch newest articles
        elif filter_type == 'most_viewed':
            queryset = queryset.order_by('-views')[:10]  # Replace 'views' with your field name
        elif filter_type == 'popular_week':
            start_of_week = timezone.now() - timezone.timedelta(days=7)
            queryset = queryset.filter(date__gte=start_of_week).order_by('-views')[:10]
        elif filter_type == 'popular_month':
            start_of_month = timezone.now() - timezone.timedelta(days=30)
            queryset = queryset.filter(date__gte=start_of_month).order_by('-views')[:10]
        return queryset


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'tags', 'photo',)
    template_name = 'article_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'summary', 'body', 'tags', 'photo',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


def tag_articles(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    articles = Article.objects.filter(tags=tag)
    return render(request, 'tag_articles.html', {'articles': articles, 'tag': tag})
