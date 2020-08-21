from django.shortcuts import render
from django.views.generic.base import View

from articles.models import Article
from .models import InvitedUser


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