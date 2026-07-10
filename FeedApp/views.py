from django.shortcuts import render, redirect
from .forms import PostForm,ProfileForm, RelationshipForm
from .models import Post, Comment, Like, Profile, Relationship
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

# When a URL request matches the pattern we just defined, 
# Django looks for a function called index() in the views.py file. 

def index(request):
    """The home page for Learning Log."""
    return render(request, 'FeedApp/index.html')


# Login Decorator
@login_required
def profile(request):
    # Wanting to grab profile from models.py and filter by user 
    # filter() works with exists()
    profile = Profile.objects.filter(user=request.user)
    # Check to see if they have a profile
    # if profile does not exist then code below runs we create one for them
    if not profile.exists(): 
        # Creating a new profile for the unidentied user
        Profile.objects.create(user=request.user)
    # We know now a profile does exist for unidentified user, so we call it using get
    profile = Profile.objects.get(user=request.user)

    # If request method is not equal to POST, method is get and we just will want to load the webpage
    if request.method != 'POST':
        # Not a blank profile, but an instance profile to update their profile
        form = ProfileForm(instance=profile)
    else:
        # request method is POST, so we want to save to the database
        form = ProfileForm(instance=profile,data=request.POST)
        if form.is_valid():
            form.save()
            # Once saved to database where should the user be redirected? 
            # keep them on the profile page
            return redirect('FeedApp:profile')

    # We now need to send the form as part of the context library
    context = {'form':form}
    return render(request, 'FeedApp/profile.html', context)





# Login Decorator
@login_required
# In my feed, we would like to see all of our posts as well as likes and comments
def myfeed(request):
    # Creating a list of comments and likes on posts
    comment_count_list = []
    like_count_list = []
    # Filter the posts retreived by the current user
    # also order the posts by date using .order_by with date_posted field from models.py
    # -date_posted puts the posts in descending order, newest to oldest
    posts = Post.objects.filter(username=request.user).order_by('-date_posted')
    # We would like to have like and comment count for each post
    for p in posts: 
        # Comment count through Comment model
        c_count = Comment.objects.filter(post=p).count()
        # Like Count
        l_count = Like.objects.filter(post=p).count()
        # Everytime we get a comment count and a like count add it to a comment count list
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    # Once zipped, we can iterate through all at the same time
    zipped_list = zip(posts,comment_count_list, like_count_list)

    context = {'posts':posts, 'zipped_list':zipped_list}
    return render(request, 'FeedApp/myfeed.html', context)





# Login Decorator
@login_required
# Creating a new function called new_post
# new post we would like to see if it is a get or post. If get then prompt a blank PostForm()
# if POST then, whatever the user filled out needs to be pushed to the database
    # in PostForm in forms.py, only fields needed are description and image
        # in models.py file class Post include 4 attributes: description, username, image and date_posted
        # however username and date_posted are autopopulated so just description and image
def new_post(request):
    # If request is not a POST form then prompt a blank one PostForm()
    if request.method != 'POST':
        form = PostForm()
    else:
        # Or if request is POST then upload to database
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            # Before saving to the database we must attached a username to it
            new_post = form.save(commit=False)
            new_post.username = request.user
            new_post.save()
            # After validating user and saving to database, redirect to myfeed page
            return redirect('FeedApp:myfeed')
        
    context = {'form':form}
    return render(request, 'FeedApp/new_post.html', context)






# Login Decorator
@login_required
def friendsfeed(request):
    # Creating a list of friends feed on posts
    comment_count_list = []
    like_count_list = []
    friends = Profile.objects.filter(user=request.user).values('friends')
    posts = Post.objects.filter(username__in=friends).order_by('-date_posted')
    
    for p in posts: 
        # Comment count through Comment model
        c_count = Comment.objects.filter(post=p).count()
        # Like Count
        l_count = Like.objects.filter(post=p).count()
        # Everytime we get a comment count and a like count add it to a comment count list
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    # Once zipped, we can iterate through all at the same time
    zipped_list = zip(posts,comment_count_list,like_count_list)


    # Checking to see if the like button was pressed:
    # if request.method ==, if the form was submitted and the button like was pressed, grab the value
    if request.method == 'POST' and request.POST.get("like"):
        # Getting the value of button called like
        post_to_like = request.POST.get("like")
        print(post_to_like)
        # Check to see if the same user already liked a post
        # checking to see if the same post has the same user
        like_already_exists = Like.objects.filter(post_id=post_to_like, username=request.user)
        # If the user and post havent already liked then create the like
        if not like_already_exists.exists():
            Like.objects.create(post_id=post_to_like,username=request.user)
            # Number of likes will go up by one
            return redirect("FeedApp:friendsfeed")


    context = {'posts':posts, 'zipped_list':zipped_list}
    return render(request, 'FeedApp/friendsfeed.html', context)





# Login Decorator
@login_required
# Creating a function comments to include attributes within the myfeed/My Posts
# this function will need a particular post_id so we know what comment belongs to what post 
    # in models.py and urls.py 
def comments(request, post_id):
    # Wanting to see if anyone has clicked on the button to comment
    # We will not be using a Form as not listed on forms.py
    # Manual function used to check if button has been pressed. the request.POST.get("btn1") function results in a true/false
    if request.method == 'POST' and request.POST.get("btn1"):
        # Gather the text elements 
        comment = request.POST.get('comment')
        # Add a new row
        # the id to each column it typically the name of the model_id such as, post_id
        Comment.objects.create(post_id=post_id,username=request.user,text=comment,date_added=date.today())

    # Now we want to display the message on the same page, get the comments from the database
    # everytime the submit button is hit to refresh the page
    comments = Comment.objects.filter(post=post_id)
    post = Post.objects.get(id=post_id)

    context = {'post':post, 'comments':comments}

    return render(request, 'FeedApp/comments.html',context)





# Login Decorator
@login_required
# Handle friend requests, sent out, received or blocked
# Admin is the first friends request, to ensure your friends from everyone
def friends(request):
    ###################### SENDER BEING USER PROFILE ######################
    # Get the admin_profile and user profile to create the first relationship
    admin_profile = Profile.objects.get(user=1)
    user_profile = Profile.objects.get(user=request.user)

    # To get My Friends
    # friends is a collection of users that is many to many within the Profile class
        #user_profile.friends.all(), list of users
        #Profile.objects.filter(user__in=user_friends), a list of user friends profiles
    user_friends = user_profile.friends.all()
    user_friends_profiles = Profile.objects.filter(user__in=user_friends)

    # To get Friend Requests sent
    # Model Relationship
        #user_relationships, is a collection of all the people that the user has sent request to.
        #request_sent_profiles, grab the receiver, collection of all profiles we sent a request to. 
    user_relationships = Relationship.objects.filter(sender=user_profile)
    request_sent_profiles = user_relationships.values('receiver')

    # To get eligilble profiles EXCLUDE: 
    # the user, 
    # their existing friends, and 
    # friend requests sent already
        # idea is to remove anyone that did not get pulled out in the above code
    all_profiles = Profile.objects.exclude(user=request.user).exclude(id__in=user_friends_profiles).exclude(id__in=request_sent_profiles)
   
   
    ###################### RECEIVER BEING USER PROFILE ######################
    # To get Friend Requests sent by the user
    # results in a list of friend request received
    request_received_profiles = Relationship.objects.filter(receiver=user_profile,status='sent')

    # PRETEND TO BE A FIRST TIME USER WITH NO FRIENDS:
    # if the this is the first time to access the friend request page, create the first relationship 
    # with the admin of the website (so the admin is friends with everyone). The code above requires at least one relationship to work

    # If the user does have an exisiting relationship, then create one.
    if not user_relationships.exists():
        # Sender is Profile
        # Receive is Profile
        Relationship.objects.create(sender=user_profile, receiver=admin_profile,status='sent')



    # Check to see WHICH submit button was pressed (sending a friends request or accepting a friend request)




    # this is to process all send requests
    if request.method == 'POST' and request.POST.get("send_requests"):
        receivers = request.POST.getlist("send_requests")
        # Want to get the receiver Profile and create the relationship object
        for receiver in receivers:
            # Gathering the profile id of the receiver
            receiver_profile = Profile.objects.get(id=receiver)
            # Creating a relationship object 
            Relationship.objects.create(sender=user_profile,receiver=receiver_profile,status='sent')
        return redirect('FeedApp:friends')
    


    # This is to process all receive requests
        # if send button do this, if request.method =='POST'
        # if receive button do this, request.POST.get()
    if request.method == 'POST' and request.POST.get("receive_requests"):
        # Get a list of people who sent us a friend request
        senders = request.POST.getlist("receive_requests")
        for sender in senders:
            # Update the relationship model for the sender to status 'accepted'
            Relationship.objects.filter(id=sender).update(status='accepted')
            # Create an relationship object to gain access the sender's user id
            # to add to the friends list of the user
            relationship_obj = Relationship.objects.get(id=sender)
            user_profile.friends.add(relationship_obj.sender.user)

            # add the user to the friends list of the sender's profile
            relationship_obj.sender.friends.add(relationship_obj.sender.user)

    context = {'user_friends_profiles':user_friends_profiles,'user_relationships':user_relationships,
               'all_profiles':all_profiles,'request_received_profiles':request_received_profiles}

    return render(request, 'FeedApp/friends.html', context)

