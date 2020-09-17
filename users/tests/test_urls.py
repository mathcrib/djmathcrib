import pytest

from mixer.backend.django import mixer
from django.urls import reverse

from users.models import InvitedUser


@pytest.mark.django_db
class TestAnonymousUserPermissions:
    """
    Тесты проверяют доступ анонимных пользователей к различным страницам сайта.
    """
    def test_anonymous_user_home_page_access(self, client):
        url = reverse('home_page')
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница "/" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_anonymous_user_create_article_access(self, client):
        url = reverse('article_create')
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert 'login/?next' in response.url

    def test_anonymous_user_article_panel_access(self, client):
        url = reverse('article_panel')
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert 'login/?next' in response.url

    def test_anonymous_user_invitations_access(self, client):
        url = reverse('invitations')
        try:
            response1 = client.get(url)
            response2 = client.post(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert 'login/?next' in response1.url
        assert 'login/?next' in response2.url

    def test_anonymous_user_profile_access(self, client):
        url = reverse('profile', kwargs={'pk': 1})
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert 'login/?next' in response.url


@pytest.mark.django_db
class TestAuthorPermissions:
    """
    Тесты проверяют доступ авторов к различным страницам сайта.
    """
    def test_author_home_page_access(self, author_client):
        url = reverse('home_page')
        try:
            response = author_client.get(url)
        except Exception as e:
            assert False, f'Страница "/" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_author_create_article_access(self, author_client):
        url = reverse('article_create')
        try:
            response = author_client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_author_article_panel_access(self, author_client):
        url = reverse('article_panel')
        try:
            response = author_client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response.status_code == 403

    def test_author_invitations_access(self, author_client):
        url = reverse('invitations')
        try:
            response1 = author_client.get(url)
            response2 = author_client.post(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response1.status_code == 403
        assert response2.status_code == 403

    def test_author_profile_access(self, author_client, author):
        new_user = mixer.blend('users.User')
        author_profile_url = reverse('profile', kwargs={'pk': author.id})
        alien_profile_url = reverse('profile', kwargs={'pk': new_user.id})
        try:
            response1 = author_client.get(author_profile_url)
            response2 = author_client.get(alien_profile_url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response1.status_code == 200
        assert response2.status_code == 403


@pytest.mark.django_db
class TestEditorPermissions:
    """
    Тесты проверяют доступ редактора к различным страницам сайта.
    """
    def test_editor_home_page_access(self, editor_client):
        url = reverse('home_page')
        try:
            response = editor_client.get(url)
        except Exception as e:
            assert False, f'Страница "/" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_editor_create_article_access(self, editor_client):
        url = reverse('article_create')
        try:
            response = editor_client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_editor_article_panel_access(self, editor_client):
        url = reverse('article_panel')
        try:
            response = editor_client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_editor_invitations_access(self, editor_client):
        url = reverse('invitations')
        try:
            response1 = editor_client.get(url)
            response2 = editor_client.post(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response1.status_code == 403
        assert response2.status_code == 403

    def test_editor_profile_access(self, editor_client, editor):
        new_user = mixer.blend('users.User')
        author_profile_url = reverse('profile', kwargs={'pk': editor.id})
        alien_profile_url = reverse('profile', kwargs={'pk': new_user.id})
        try:
            response1 = editor_client.get(author_profile_url)
            response2 = editor_client.get(alien_profile_url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response1.status_code == 200
        assert response2.status_code == 403


@pytest.mark.django_db
class TestModeratorPermissions:
    """
    Тесты проверяют доступ модератора к различным страницам сайта.
    """
    def test_moderator_home_page_access(self, moderator_client):
        url = reverse('home_page')
        try:
            response = moderator_client.get(url)
        except Exception as e:
            assert False, f'Страница "/" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_moderator_create_article_access(self, moderator_client):
        url = reverse('article_create')
        try:
            response = moderator_client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_moderator_article_panel_access(self, moderator_client):
        url = reverse('article_panel')
        try:
            response = moderator_client.get(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response.status_code == 200

    def test_moderator_invitations_access(self, moderator_client, moderator):
        url = reverse('invitations')
        try:
            response1 = moderator_client.get(url)
            response2 = moderator_client.post(url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response1.status_code == 200
        assert InvitedUser.objects.filter(inviting=moderator).exists()

    def test_moderator_profile_access(self, moderator_client, moderator):
        new_user = mixer.blend('users.User')
        author_profile_url = reverse('profile', kwargs={'pk': moderator.id})
        alien_profile_url = reverse('profile', kwargs={'pk': new_user.id})
        try:
            response1 = moderator_client.get(author_profile_url)
            response2 = moderator_client.get(alien_profile_url)
        except Exception as e:
            assert False, f'Страница "{url}" работает неправильно. Ошибка: {e}'
        assert response1.status_code == 200
        assert response2.status_code == 403
