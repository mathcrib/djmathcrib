from articles.models import Article


def get_category_tree(request):
    category_roots = Article.published_objects.filter(level=1)
    return {'categories': category_roots}
