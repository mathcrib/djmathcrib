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
    template_name = 'article_list.html'
    model = Article
    paginate_by = 10
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        return Article.objects.filter(Q(text__contains=q)|Q(title__contains=q))


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
