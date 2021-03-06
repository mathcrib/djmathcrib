from django.urls import path

from .views import (
    InvitationView,
    ModeratorControlPanelView,
    SignUpView,
    UserProfileView
)

urlpatterns = [
    path('panel/', ModeratorControlPanelView.as_view(), name='article_panel'),
    path('invitations/', InvitationView.as_view(), name='invitations'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
]
