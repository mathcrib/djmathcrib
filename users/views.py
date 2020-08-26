from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from django.views.generic.base import View

from articles.models import Article

from .forms import CreationForm
from .models import InvitedUser
from .utilits import invite_key_generator


class ModeratorControlPanelView(View):

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(
            is_category=False
        ).order_by('is_published', '-created')
        context = {
            'articles': articles,
        }
        return render(request, 'users/control_panel.html', context=context)


class InvitationView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'invited': InvitedUser.objects.all()
        }
        return render(request, 'users/invitation.html', context=context)

    def post(self, request, *args, **kwargs):
        invite_key = invite_key_generator(length=20)
        invite_url = request.build_absolute_uri(
            f'/users/signup/?key={invite_key}',
        )
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
                'form': CreationForm(),
                'key': key,
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
        key = request.POST.get('key', None)
        if key:
            form = CreationForm(request.POST)
            invite = get_object_or_404(
                InvitedUser,
                invite_key=key,
                invited=None,
            )
            if form.is_valid():
                user = form.save()
                invite.invited = user
                invite.save()
                return redirect('login')
            return render(request, 'users/signup.html', {'form': form})
        raise Http404('Такой страницы не существует.')
