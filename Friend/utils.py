from Friend.models import FriendRequest

# checking if friend request exists
def get_friend_request_or_false(sender , receiver):
    try:
        # if friend request exists
        return FriendRequest.objects.get(sender = sender , receiver =receiver ,is_active = True)
    except FriendRequest.DoesNotExist:
        #otherwise this
        return False