

############# ALLOWS TO CREATE DATABASE TABLES ##############
    ############# STORES THE DATA ##############

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Associating each profile to a user and once we know the user we can get their profile
# friends = many to many; can have many friends
class Profile(models.Model):
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    email = models.EmailField(max_length=300,blank=True)
    dob = models.DateField(null=True,blank=True)
    bio = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True,related_name='friends')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    # String method will return a user name from the user field
    def __str__(self):
        return f"{self.user.username}"



# Status Choices: when sending a friend request out
STATUS_CHOICES = (
    ('sent','sent'),
    ('accepted','accepted')
)




# Relationship model: allows us to create a relationship between two profiles 
# sender & received are Foreign Keys to the profile class
# The way it works: 
    # As a user we want to send a friend request, will be the sender
    # receiver is someone else in our network we want to be friends with 
    # status of the relationship is default="send"
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="sent")
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)




# Post class: related to any post that includes a description, username (who is making this module), image (requires pillow)
# (User, on_delete=models.CASCADE), delete the User, delete all of the Profiles posts,likes, etc. prevents orphaned records
class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    # All images will be uploaded to the images folder
    # they are not required to have an image with every post so we use blank=True
    image = models.ImageField(upload_to='images',blank=True)
    # Recording post date
    date_posted = models.DateTimeField(auto_now_add=True)

    # String method will return the description of the post
    def __str__(self):
        return self.description





# Comment is associated with a post
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)

    # String method will return the text of the comment
    def __str__(self):
        return self.text
    
# To keep track who liked a post
# records username of user who liked the post
# records what post was liked by the post
class Like(models.Model):
    username = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

