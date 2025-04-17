from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    pic = models.URLField(blank=True, null=True, default="https://ichef.bbci.co.uk/ace/standard/2560/cpsprodpb/b2d0/live/d4d933e0-8a17-11ef-bfd3-790fcba1cccf.jpg")  # External image URL
    created_date = models.DateTimeField(default=now, editable=False)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} | By: {self.author} | ID: {self.id}'


    def delete(self, *args, **kwargs):
        # Delete all likes and comments related to the post
        Like.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id).delete()
        Comment.objects.filter(post=self).delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.title} | By: {self.author} | ID: {self.id} | Content Type: {ContentType.objects.get(model="post").id}'



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now, editable=False)
    likes_count = models.PositiveIntegerField(default=0)

    def delete(self, *args, **kwargs):
        #delete all comment likes before deleting itself
        Like.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id).delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.post:
            self.post.likes_count = Like.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=self.post.id).count()
            self.post.save()

    def __str__(self):
        return f'{self.author.username}: {self.content} | ID: {self.id}'
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        #only one like from each user
        unique_together = ('user', 'content_type', 'object_id')

    def delete(self, *args, **kwargs):
        # Update like count before deleting
        if isinstance(self.content_object, Post):
            self.content_object.likes_count = Like.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=self.content_object.id).count()
            self.content_object.save()
        elif isinstance(self.content_object, Comment):
            self.content_object.likes_count = Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=self.content_object.id).count()
            self.content_object.save()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update likes count for the associated content object
        if isinstance(self.content_object, Post):
            self.content_object.likes_count = Like.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id=self.content_object.id).count()
            self.content_object.save()
        elif isinstance(self.content_object, Comment):
            self.content_object.likes_count = Like.objects.filter(content_type=ContentType.objects.get_for_model(Comment), object_id=self.content_object.id).count()
            self.content_object.save()


    def __str__(self):
        return f'{self.user} liked {self.content_object}'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Hey there!")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    avatar_url = models.URLField(default="https://static.vecteezy.com/system/resources/previews/005/544/718/non_2x/profile-icon-design-free-vector.jpg")

    def get_avatar(self):
        return self.avatar_url if self.avatar_url else self.avatar.url

    def __str__(self):
        return f'{self.user} - {self.bio}'

