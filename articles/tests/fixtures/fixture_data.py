import pytest

from mixer.backend.django import mixer


@pytest.fixture
def article():
    return mixer.blend('articles.Article')
