from django.urls import path
from . import views

app_name = 'FeedApp'

urlpatterns = [
    path('', views.index, name='index'),
    # Creating Profile URL
    path('profile/', views.profile, name='profile'),
    # Creating a pathway to myfeed to only view details of that users feed
    path('myfeed', views.myfeed, name='myfeed'),
    # Creating a pathway URL to new_posts
    path('new_post/', views.new_post, name='new_post'),
    # Creating pathway for friendsfeed
    path('friendsfeed', views.friendsfeed, name='friendsfeed'),
    # Creating pathway for Comments
    path('comments/<int:post_id>/', views.comments, name='comments'),
    # Creating pathway for friends
    path('friends/', views.friends, name='friends'),
    ]

    