from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    picture = models.ImageField(null=True, blank=True)
    created_date = models.DateTimeField(default=now, editable=False)
    likes = models.ManyToManyField(User, related_name='liked_posts', default=None)


    def __str__(self):
        return f'{self.title} | By: {self.author} | ID: {id(self)} '


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now, editable=False)
    likes = models.ManyToManyField(User, related_name='liked_comments', default=None)


    def __str__(self):
        return f'{self.author}: {self.content}'
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) #type of object
    object_id = models.PositiveIntegerField() #object ID
    content_object = GenericForeignKey('content_type', 'object_id') #can be post or comment

    def __str__(self):
        return f'{self.user}: {self.content_object} || {self.content_type}'
    

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.bio}'