from argparse import ArgumentParser
import pandas as pd
import random
from random import randrange
from datetime import timedelta
from datetime import datetime
import math

# Parse the arguments
parser = ArgumentParser()
parser.add_argument("-users", dest="max_users", type=int,
                    help="Specify the number of user of the social media")

parser.add_argument('-minfriends', dest="min_friends", type=int,
                    help="Specify the minimum number of friends for each users")

parser.add_argument('-maxfriends', dest="max_friends", type=int,
                    help="Specify the maximum number of friends for each users")

parser.add_argument('-startdate', dest="start_date", 
                    help="Specify the lower bound of the date for the friendship invitations and video sharing, please follow the following format 'Month/Day/Year', for example '1/1/2014 1:30 PM'")

parser.add_argument('-enddate', dest="end_date", 
                    help="Specify the high bound of the date for the friendship invitations and video sharing, please follow the following format 'Month/Day/Year', for example '1/1/2016 1:30 PM'")

parser.add_argument('-maxvideo', dest="max_video", type=int,
                    help="Specify the maximum number of video per users")   

parser.add_argument('-maxlike', dest="max_like", type=int,
                    help="Specify the maximum number of likes")                               

args = parser.parse_args()

nb_users = args.max_users

# Generate Friendship
user_id = []
friend_id = []

for n_user in range(nb_users):
    num_friends = random.randint(args.min_friends,args.max_friends)
    friends = []
    for n_friend in range(num_friends):
        buddy_id = random.randint(1, num_friends)
        friends_choices = [i for i in range(1, nb_users) if i not in friends]
        friend_index = random.choice(friends_choices)
        friends.append(friend_index)
    for friend in friends:
        user_id.append(n_user)
        friend_id.append(friend)

friendship_df = pd.DataFrame({'user_id': user_id, 'friend_id': friend_id})
friendship_df.to_csv('friendship.csv', index=False)

# Generate Sent Friendship invitation
def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

acceptor_id = []
requestor_id = []
time = []

for row in friendship_df.itertuples():
    user_id = row[2]
    friend_id = row[1]
    acceptor_id.append(friend_id)
    requestor_id.append(user_id)
    
    d1 = datetime.strptime(args.start_date, '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime(args.end_date, '%m/%d/%Y %I:%M %p')
    generated_date = random_date(d1,d2)
    
    time.append(generated_date)
    
accepted_df = pd.DataFrame({'accepter_id': acceptor_id, 'requester_id': requestor_id, 'time': time})
accepted_df.to_csv('accepted-request.csv', index=False)

# Generate Accepted Friendship invitation
requester_id = []
sent_to_id = []
request_time = []

users_id = [n for n in range(nb_users)]
for user_id in users_id:
    accepted_requests = list(accepted_df[accepted_df['requester_id'] == user_id]['accepter_id'])
    accepted_requests_time = list(accepted_df[accepted_df['requester_id'] == user_id]['time'])
    # Generate number of total requests
    num_requests = math.ceil(len(accepted_requests) * (random.uniform(0.2,1.5)))
    potential_refused_requests = [n for n in range(nb_users) if n not in accepted_requests]
    sent_requests = [random.choice(potential_refused_requests) for x in range(num_requests)]
    
    time_index = 0
    for accepted_r in accepted_requests:
        requester_id.append(user_id)
        sent_to_id.append(accepted_r)
        request_time.append(accepted_requests_time[time_index])
        time_index += 1
        
    for refused_r in sent_requests:
        requester_id.append(user_id)
        sent_to_id.append(refused_r)
        d1 = datetime.strptime(args.start_date, '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime(args.end_date, '%m/%d/%Y %I:%M %p')
        generated_date = random_date(d1,d2)
        request_time.append(generated_date)
    
request_sent_df = pd.DataFrame({'requester_id': requester_id, 'sent_to_id': sent_to_id, 'time': request_time})
request_sent_df.to_csv('requests-sent.csv', index=False)

# Generate Video Sharing data
users_id = [user for user in range(nb_users)]
publisher_id = []
video_id = []
video_duration = []
video_date = []
# Define 100,000 videos IDs
v_ids = [n for n in range(100000)]

for user_id in users_id:
    # Number of video per user
    num_video = random.randint(1, args.max_video)
    # Create n video per users with an ID from 1 to 1000
    # And a duration from 1 to 3600 seconds
    for num_v in range(num_video):
        # Pick a video ID from v_ids and remove it for the available IDs
        v_id = random.choice(v_ids)
        v_ids.remove(v_id)
        
        v_duration = random.randint(1,3600)
        video_id.append(v_id)
        video_duration.append(v_duration)
        publisher_id.append(user_id)
        
        d1 = datetime.strptime(args.start_date, '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime(args.end_date, '%m/%d/%Y %I:%M %p')
        generated_date = random_date(d1,d2)
        video_date.append(generated_date)
        
video_df = pd.DataFrame({'publisher_id': publisher_id, 'video_id': video_id, 'video_duration': video_duration, 'video_date': video_date})
video_df.to_csv('video.csv', index=False)

# Generate Users Interaction with the Videos
video_id = []
user_id = []
user_timespend = []

users_id = [user for user in range(nb_users)]

videos = list(video_df.video_id.unique())
for video in videos:
    # Number of likes
    num_likes = random.randint(1, args.max_like)
    likes = random.sample(users_id, num_likes)
    for like in likes:
        # Random user who likes the video
        video_id.append(video)
        user_id.append(like)
        timespend = random.randint(1,7200)
        user_timespend.append(timespend)
        
interaction_df = pd.DataFrame({'video_id': video_id, 'user_id': user_id, 'user_timespend': user_timespend})
interaction_df.to_csv('video-interaction.csv', index=False)


