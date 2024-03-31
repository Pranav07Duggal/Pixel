from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class FriendList(models.Model):

    user            = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , related_name ='user') 
    friends         = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True , related_name = 'friend')

    def __str__(self):
        return self.user.username
    
    #add new friend
    #with self we are accessing the current instances
    #account is other user 

    def add_friend(self,account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.friends.save()

    # remove friend
            
    def remove_friend(self,account):
        if account in self.friends.all():
            self.friends.remove(account)

    # terminate friendship 
    
    def unfriend(self,removee):
        if removee in self.friends.all():
            remover = self

            # remove from remover friend list 
            
            remover.remove_friend(removee)
            
            # remove from removee friend list

            friend_list = FriendList.objects.get(user = removee)
            friend_list.remove_friend(remover.user)  

    # is my friend

    def is_mutual_friend(self , friend):

        if friend in self.friends.all():
            return True

    # friend requests
        
class FriendRequest(models.Model):

    sender      = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE ,related_name = 'sender')
    receiver    = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE ,related_name = 'receiver')

    # friend request is active or not , it become inactive when i is accepted or declined
    is_active   =models.BooleanField(blank = True , null = False , default = True)
    
    # add time of follow
    timestamp   =models.DateTimeField(auto_now_add=True)
    
    # nothing just naming the row ,(not working)
    # def __str__(self):
    #         self.sender.username

    def accept(self):
        
        # adding user to receiver friend list 
        receiver_friend_list = FriendList.objects.get(user = self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            
            # adding user to sender friend list
            sender_friend_list = FriendList.objects.all(user = self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                # for the accept or decline button 
                self.is_active = False
                self.save()

    # for decline button 
                
    def decline(self):
        self.is_active = False
        self.save()

    # may get canceled by sender or receiver (unfollow)     
    def cancel(self):
        self.is_active =False
        self.save()
