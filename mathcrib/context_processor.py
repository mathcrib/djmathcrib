from articles.models import Article


def get_category_tree(request):
    category_roots = Article.published_objects.prefetch_related('children')
    return {'category_tree': category_roots}
