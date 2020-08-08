from django.shortcuts import get_object_or_404, render

from .models import Article


def get_next(request, id=None):
    if id is None:
        next = Article.objects.root_nodes()
    else:    
        next = get_object_or_404(Article, pk=id).get_children()
    return render(request, "index.html", {"next": next})


def get_article(request, id):
    article = get_object_or_404(Article, pk=id)
    author = article.author.username
    return render(
        request, 
        "index.html", 
        {"article": article, "author":author}
    )
