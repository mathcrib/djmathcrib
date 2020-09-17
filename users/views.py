from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from django.views.generic.base import View

from articles.models import Article
from emails.sender import send_email

from .forms import CreationForm
from .models import InvitedUser, User
from .utilits import invite_key_generator


class ModeratorControlPanelView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_personal:
            return HttpResponseForbidden()

        articles = Article.objects.filter(is_category=False).order_by(
            'is_published',
            '-created'
        )
        context = {
            'articles': articles,
        }
        return render(request, 'users/control_panel.html', context=context)


class InvitationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_administration:
            return HttpResponseForbidden()

        context = {
            'invited': InvitedUser.objects.all()
        }
        return render(request, 'users/invitation.html', context=context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_administration:
            return HttpResponseForbidden()

        invite_key = invite_key_generator(length=20)
        site = get_current_site(request)
        invite_url = site.domain + f'/users/signup/?key={invite_key}'

        InvitedUser.objects.create(
            inviting=request.user,
            invite_url=invite_url,
            invite_key=invite_key,
        )
        return redirect('invitations')


class SignUpView(CreateView):
    form = CreationForm()

    def get(self, request, *args, **kwargs):
        """
        Перейти на страницу регистрации можно только с валидным ключом. Ключ
        считается валидным, если после создания по нему не было регистраций.
        """
        key = request.GET.get('key', None)
        if key is None:
            raise Http404('Такой страницы не существует.')
        invite = get_object_or_404(InvitedUser, invite_key=key)
        if invite.invited is None:
            context = {
                'form': CreationForm(initial={'invite_key': key})
            }
            return render(request, 'users/signup.html', context=context)
        raise Http404('Такой страницы не существует.')

    def post(self, request, *args, **kwargs):
        """
        Проверяем, что запись с переданным ключом существует в базе, и что по
        нему еще не было регистраций.
        Создаем пользователя, а затем отмечаем, что регистрация по данному
        ключу состоялась.
        """

        form = CreationForm(request.POST)

        if form.is_valid():
            key = form.cleaned_data.get('invite_key', None)
            invite = get_object_or_404(
                InvitedUser,
                invite_key=key,
                invited=None,
            )

            user = form.save()
            invite.invited = user
            invite.save()

            data = (
                settings.DEFAULT_FROM_EMAIL,
                user.email,
                'Добро пожаловать!',
                '''<h1>Привет!</h1>
                    <p>Добро пожаловать в команду <a href="https://mathcrib.space/">mathcrib.space</a>!</p>'''
            )
            send_email(*data)
            return redirect('login')
        return render(request, 'users/signup.html', {'form': form})


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)

        if request.user != user:
            return HttpResponseForbidden()

        articles = Article.objects.filter(
            author=user_id,
            is_category=False
        ).order_by(
            '-created',
        )
        context = {
            'articles': articles,
            'user': user,
        }
        return render(request, 'users/user_profile.html', context=context)
