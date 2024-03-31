from django.shortcuts import render
from .models import Profile
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate , login , logout 
from django.http import HttpResponseRedirect , JsonResponse
from django.contrib.auth.decorators import login_required
import os
from Friend.models import FriendList ,FriendRequest
from Friend.utils import get_friend_request_or_false
from Friend.friend_request_status import FriendRequestStatus
from Project import settings
# Create your views here.

def Home(requests):
    return render(requests, 'home.html',{'text':'home'})

def Signup(requests):
    if requests.method == 'POST':
        data = requests.POST
        
        email = data.get('email')
        username = data.get('username')
        first_name =data.get('first_name')
        last_name = data.get('last_name')
        college =data.get('college')
        image = requests.FILES.get('image')
        password = data.get('password') 
        
        if email is None:
            messages.info(requests , 'Please Enter Email')
            return HttpResponseRedirect('/sign_up')
        
        if username is None:
            messages.info(requests , 'Please Enter Username')
            return HttpResponseRedirect('/sign_up')
        
        if password is None:
            messages.info(requests , 'Please Enter Password')
            return HttpResponseRedirect('/sign_up')

        if college is None:
            messages.info(requests , 'Please specify your college')
            return HttpResponseRedirect('/sign_up')

        user = Profile.objects.filter(Q(username = username) | Q(email = email))



        if user.exists():
            messages.info(requests , 'Email or Username already exists')
            return HttpResponseRedirect('/sign_up')

        obj = Profile.objects.create(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            college = college,
            prof_image = image, 
        )   



        obj.set_password(password)
        obj.save()
        obj.prof_image = image
        obj.save()

        if obj is None:
            messages.info(requests,'Some problem occur')
            return HttpResponseRedirect('/sign_up')
            
        else:
            messages.info(requests,'Sucessfully created')
            return HttpResponseRedirect('/log_in')

    return render(requests,'signup.html') 
 

def Login(requests):

    k=requests.user
    if k.is_authenticated:
        return HttpResponseRedirect('/')
    
    
    if requests.method =='POST':
        data = requests.POST
                
        email = data.get('email')
        password = data.get('password')

        if email is None:
            messages.info(requests,'email is required')
            
        if password is None:
            messages.info(requests,'password is required')

        check = Profile.objects.filter(email = email)

        # if check.is_active == False:
        #     messages.error(requests ,'email is blocked')
        #     return HttpResponseRedirect('/log_in')
        
        if check is None:
            messages.error(requests ,'email does not exists')
            return HttpResponseRedirect('/log_in')
                        
        else:
            user = authenticate(email=email,password=password)
            print(user)
            if user:
                login(requests,user)
                return HttpResponseRedirect('/')
            else:
                messages.error(requests ,'invalid credentials')
                return HttpResponseRedirect('/log_in')
            
    return render(requests ,'login.html')



def Log_out(request):
    logout(request)
    return HttpResponseRedirect('/')
            
@login_required

def Profile_page(requests, pk):
    author = Profile.objects.get(id=pk)

    # Remove the redundant initialization of friend_list here
    try:
        friend_list = FriendList.objects.get(user=author)
    except FriendList.DoesNotExist:
        friend_list = FriendList(user=author)
        friend_list.save()

    friends = friend_list.friends.all()
    context = {'friends': friends}
    is_self = True
    is_friend = False
    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    friend_requests = None
    user = requests.user
    request_send = None  # Initialize request_send

    if user.is_authenticated and user != author:
        is_self = False

        if friends.filter(pk=user.id).exists():  # Use exists() to check if the user is in friends
            is_friend = True
        else:
            is_friend = False
            friend_request_received = get_friend_request_or_false(sender=author, receiver=user)
            friend_request_sent = get_friend_request_or_false(sender=user, receiver=author)

            if friend_request_received:
                request_send = FriendRequestStatus.THEM_SENT_TO_YOU.value
                context['pending_request'] = friend_request_received.id
            elif friend_request_sent:
                request_send = FriendRequestStatus.YOU_SEND_TO_THEM.value
            else:
                request_send = FriendRequestStatus.NO_REQUEST_SENT.value

    elif not user.is_authenticated:
        is_self = False

    else:
        try:
            friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            context['friend_requests'] = friend_requests
        except Exception as e:
            print(f"Error fetching friend requests: {e}")

    context['is_self'] = is_self
    context['is_friend'] = is_friend
    # context['BASE_URL'] = settings.BASE_URL
    context['request_sent'] = request_send

    # Assuming 'auth' is the author instance, not a queryset
    context['auth'] = author

    return render(requests, 'profile.html', context)


def search(requests):
    t=list()
    search = requests.GET.get('search')        
    if search:
            result = Profile.objects.filter(Q(username__contains = str(search)) | Q(username__startswith = str(search)) | Q(username__endswith = str(search)))
            for res in result:
                if res.prof_image:
                    t.append(dict(
                            {
                            'username':res.username,
                            'profile_pic':res.prof_image.url,
                            }
                            ))
                else:
                    t.append(dict(
                            {
                            'username':res.username,
                            'profile_pic':None,
                            }
                            ))

            return JsonResponse({
            'payload' : t
            })
    print(t)
    top = Profile.objects.all()
    return render(requests,'search_user.html',{'top':top})

@login_required

def Update(requests,pk):
    obj = Profile.objects.get(id = pk)

    if requests.method == 'POST':
        data = requests.POST

        if data:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            username = data.get('username')
            college = data.get('college')
            bio = data.get('bio')
            prof_image = requests.FILES.get('prof_image')
            hide_email = data.get('hide_email')
        
            obj.first_name = first_name
            obj.last_name = last_name
            obj.username = username
            obj.college  = college
            obj.bio = bio
            obj.id = obj.id

            if prof_image:
                obj.prof_image = prof_image
            else:
                obj.prof_image = obj.prof_image
        
            if str(hide_email) == 'on':
                obj.hide_email = True

            else:
                obj.hide_email = False

            obj.save()

            return HttpResponseRedirect(f'/{obj.id}/profile/')    
    return render(requests , 'update.html' , {'u_data':obj})

        








    







