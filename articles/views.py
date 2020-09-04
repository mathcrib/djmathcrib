from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Article


def home_page(request):
    return render(request, 'index.html')


class ArticleListView(ListView):
    model = Article
    queryset = Article.published_objects.get_articles().select_related(
        'author',
    )


class ArticleDetailView(DetailView):
    model = Article

    def get_queryset(self):
        """
        Для всех доступны только опубликованные статьи. Статью на модерации
        может просматривать только автор и персонал сайта.
        """
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            if self.request.user.is_personal or self.request.user == qs.author:
                return qs
        return qs.filter(is_published=True)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'text', 'parent')
    redirect_field_name = 'next'
    login_url = '/login/'

    def form_valid(self, form):
        """
        Добавляем автора статьи перед валидацией и сохранением.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'text', 'parent', 'is_published')
    login_url = '/login/'

    def test_func(self):
        """
        Доступ разрешен только автору статьи и персоналу сайта.
        """
        obj = self.get_object()
        return self.request.user == obj.author or self.request.user.is_personal

    def form_valid(self, form):
        """
        Если статью изменяет автор, то она снимается с публикации.
        """
        if not self.request.user.is_personal:
            form.instance.is_published = False
        return super().form_valid(form)
