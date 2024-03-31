from enum import Enum
# creating states of the profile page  
class FriendRequestStatus(Enum):
    NO_REQUEST_SENT =-1
    THEM_SENT_TO_YOU = 0 
    YOU_SEND_TO_THEM = 1