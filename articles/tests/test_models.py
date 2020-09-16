import pytest

from mixer.backend.django import mixer


@pytest.mark.django_db
class TestArticleModel:

    def test_article_instance_exists(self):
        article = mixer.blend('articles.Article')
        assert article.id == 1
