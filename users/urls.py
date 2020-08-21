from django.urls import path

from .views import ModeratorControlPanelView, InvitationView

urlpatterns = [
    path('panel/', ModeratorControlPanelView.as_view(), name='article_panel'),
    path('invitations/', InvitationView.as_view(), name='invitations'),
]