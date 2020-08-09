from django.shortcuts import get_object_or_404, render

from .models import Article


def get_next(request, id=None):
    if id is None:
        next_article = Article.objects.root_nodes()
    else:    
        next_article = get_object_or_404(Article, pk=id).get_children()
    return render(request, "index.html", {"next": next_article})


def get_article(request, id):
    article = get_object_or_404(Article, pk=id)
    author = article.author.username
    return render(
        request, 
        "index.html", 
        {"article": article, "author":author}
    )
