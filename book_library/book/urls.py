from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('book_list/book/<slug:slug>/', BookDetailView.as_view(), name='book_detail'),
    path('add_book/', BookCreateView.as_view(), name='book_create'),
    path('book_list/book/<slug:slug>/edit', BookUpdateView.as_view(), name='book_update'),
    path('book_list/book/<slug:slug>/detele', BookDeleteView.as_view(), name='book_delete'),
    path('register', RegisterUser.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('profile/<str:username>', UserProfileView.as_view(), name='user_profile'),
    path('add_author', AuthorAddView.as_view(), name='add_author'),
    path('support/', support, name='support'),
    path('support/thanks/', SupportThanks.as_view(), name='support_thanks'),
]