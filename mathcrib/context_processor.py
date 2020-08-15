from articles.models import Article


def get_category_tree(request):
    category_roots = Article.objects.root_nodes().prefetch_related('children')
    return {'category_tree': category_roots}
