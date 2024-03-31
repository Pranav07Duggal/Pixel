from django.shortcuts import render
from django.http import HttpResponseRedirect ,JsonResponse
import json 
from django.contrib import messages
from User_profile.models import Profile
from Friend.models import FriendRequest
from django.db.models import Prefetch

# views here.

def send_friend_request(requests):
    # user login
    user = requests.user   

    # data that is going to be sent
    payload = {'response':None , 'messages':messages.info(requests,'request sent')}
    
    # checking ajax request is post
    if requests.method == 'POST' and user.is_authenticated:
        
        # getting receiver id when sender hit follow
        user_id = requests.POST.get('receiver_user_id')
        
        if user_id:
            
            # getting receiver data from database
            receiver =  Profile.objects.get(pk = user_id)
            
            # try some stuff
            try :
                
                # getting the relation of sender and receiver from friend list
                friend_requests = FriendRequest.objects.filter(sender = user, receiver = receiver) 
                
                try:
                    # if relation in friendlist 
                    for requests in friend_requests:
                        if requests.is_active:
                            raise Exception('you already sent them a friend requests.')
                    
                    # if no relation exists then create one 
                    friend_requests = FriendRequest(sender = user , receiver = receiver)
                    friend_requests.save()
                    payload['response'] = 'friend request sent'
                
                # if something wrong raise exception
                except Exception as e :
                    payload['response'] = str(e) 
            
            # if no relation exists then make one 
            except FriendRequest.DoesNotExist :
                friend_requests = FriendRequest(sender = user , receiver = receiver)
                friend_requests.save()
                payload['response'] = 'friend request sent'

            # if nothing come in payload 
            if payload['response'] == None:
                payload['response'] = 'something went wrong'
            
            # if no user exists
            # else:
            #     payload['response'] = 'Unable to send a friend request.'
        
        # if user not authenticated
        else:
            payload['response']= 'you must be authenticated to send a friend request.'

        # using dumps here not dump because payload is a string
        return HttpResponseRedirect(json.dumps(payload) , content_type = 'application/json')

def  cancel_requests(requests):
    print(requests)
    user = requests.user
    if requests.method == 'POST' and user.is_authenticated:
        user_id = requests.POST.get('receiver_user_id')
        receiver =  Profile.objects.get(pk = user_id)
        friend_requests = FriendRequest.objects.filter(sender = user, receiver = receiver)
        friend_requests.delete()

    else:
        raise Exception('something wrong')
    
    return messages.info(requests,'request cancelled')

# sending accept decline request to user
def notify_user(requests):
    user = requests.user
    notify = FriendRequest.objects.filter(receiver_id=user.id , is_active = True)
    notify_list= list(notify.values('sender_id' , 'timestamp'))
    sr =[]
    for no in notify_list:
        sender_data = Profile.objects.filter(id = no['sender_id'])
        sender_dict = list(sender_data.values('id','username','prof_image','college'))
        sr.append(sender_dict)
        
    payload = {'data':notify_list ,'profile':sr}

    return JsonResponse(payload)

def decline(requests,pk):
    user = requests.user
    if requests.method == 'POST' and user.is_authenticated:
        sender_id = pk
        k = FriendRequest.objects.filter(sender_id=sender_id , is_active=True , receiver_id = user)
        s=k
        k.delete()
        print(list(s.values()))
        payload = {'da':list(s.values())}
    return JsonResponse(payload)

def accept(requests , *args , **kwargs):
    user = requests.user
    payload = {}
    if requests.method == 'GET' and user.is_authenticated:
        friend_request_id = kwargs.get('friend_request_id')
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk = friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.is_active = False
                    payload['response'] = 'Friend request accepted'
                
                else:
                    payload['response'] = 'something wrong'
        
            else:
                payload['response']='Thats not your request to accept'
        else:
            payload['response']='unable to accept'
    else:
        payload['response']='must be authenticated'

    return HttpResponseRedirect(json.dumps(payload))

            






0