from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import AuthorUpdateForm, PersonalUpdateForm
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
        id = self.kwargs.get('pk')
        qs = Article.objects.filter(id=id)

        obj = qs.first()

        if self.request.user.is_authenticated:
            if self.request.user.is_personal or self.request.user == obj.author:
                return qs
        if obj.is_published:
            return qs
        else:
            raise Http404


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'text', 'parent')
    redirect_field_name = 'next'
    login_url = '/auth/login/'

    def form_valid(self, form):
        """
        Добавляем автора статьи перед валидацией и сохранением.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = PersonalUpdateForm
    author_form_class = AuthorUpdateForm
    redirect_field_name = 'next'
    login_url = '/auth/login/'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        obj = self.get_object()
        if not self.request.user.is_personal:
            context['author'] = obj.author
            context['form'] = self.get_form(self.author_form_class)
        return context
