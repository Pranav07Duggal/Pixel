from django.urls import path
from Friend.views import(
    send_friend_request,
    cancel_requests,
    notify_user,
    decline
)

app_name = 'Friend'

urlpatterns = [
    path('friend_request/' , send_friend_request , name='friend-request'),
    path('cancel_request/', cancel_requests ,name ='friend-request-cancel'),
    path('tdlgrklfoxxhmjapawjluirdcdlpjfhh/notify/',notify_user,name='friend-notify'),
    path('decline/<int:pk>/',decline,name='decline')
]