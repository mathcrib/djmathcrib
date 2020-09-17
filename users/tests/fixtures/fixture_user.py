import pytest

from mixer.backend.django import mixer

from users.models import UserRole


@pytest.fixture
def author():
    return mixer.blend('users.User')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def editor():
    return mixer.blend('users.User', role=UserRole.EDITOR)


@pytest.fixture
def editor_client(editor, client):
    client.force_login(editor)
    return client


@pytest.fixture
def moderator():
    return mixer.blend('users.User', role=UserRole.MODERATOR)


@pytest.fixture
def moderator_client(moderator, client):
    client.force_login(moderator)
    return client
