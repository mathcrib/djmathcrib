from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Article


def get_next(request, id=None):
    if id is None:
        next_article = Article.objects.root_nodes()
    else:
        next_article = get_object_or_404(Article, pk=id).get_children()
    return render(request, "index.html", {"next": next_article})


def home_page(request):
    return render(request, "home.html")


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        q = self.request.GET.get('q', None)

        if q is None:
            return Article.objects.filter(text__isnull=False)

        separate = self.request.GET.get('separate', None)
        if separate is None:
            return Article.objects.filter(
                   Q(text__icontains=q) | Q(title__icontains=q))
                   
        ids = set()
        for query in q.split():
            queryset = set(Article.objects.filter(
                Q(text__icontains=query) | Q(title__icontains=query)
                ).values_list('pk', flat=True))
            print(queryset)
            ids = ids.union(queryset)
        return Article.objects.filter(pk__in=ids)


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'text', 'parent')
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'text', 'parent')
