from articles.models import Article


def get_category_tree(request):
    category_roots = Article.objects.filter(
        is_published=True, level=1
    ).prefetch_related('children')
    return {'category_tree': category_roots}
