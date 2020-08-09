from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Article


def get_next(request, id=None):
    if id is None:
        next_article = Article.objects.root_nodes()
    else:
        next_article = get_object_or_404(Article, pk=id).get_children()
    return render(request, "index.html", {"next": next_article})


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'text', 'parent')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'text', 'parent')
