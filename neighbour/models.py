from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

import datetime as dt
# Create your models here.

class Profile(models.Model):
    class Meta:
        db_table = 'profile'
    bio = models.TextField(max_length=200, null=True, blank=True, default="bio")
    pic = models.ImageField(upload_to='image/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name="profile")
    
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
        
    @classmethod
    def search_profile(cls, name):
        profiles = cls.objects.filter(user__username__icontains=name)
        return profiles
    
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id).first()
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile
    
    def __str__(self):
        return self.user.username


class Image(models.Model):
    class Meta:
        ordering = ('-post_date',)
    image = models.ImageField(upload_to = 'image/',)
    title = models.CharField(max_length=60)
    post = HTMLField()
    poster = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, related_name="images")
    post_date = models.DateTimeField(auto_now_add=True)
    project_url=models.URLField(max_length=250)
    comments= models.TextField(blank=True)
    
    def save_image(self):
        self.save()
    
    def delete_image(self):
        self.delete()
        
    def update_image(self):
        self.update_image()
        
    @classmethod
    def get_all_images(cls):
        all_images = Image.objects.all()
        return all_images
    
    @classmethod
    def search_images(cls, search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects
        
    @classmethod
    def get_image_id(cls, id):
        image = Image.objects.get(pk=id)
        return image
    
    @classmethod
    def get_profile_images(cls, profile):
        images = Image.objects.filter(profile__pk = profile)
        return images
    

    @classmethod
    def filter_by_category(cls, filter_category):
        images_category = Image.objects.filter(category__id=filter_category)
        return images_category   
        
    def __str__(self):
        return self.name
    
class Comments(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='user')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="images")
    comment = models.TextField()

    def save_comment(self):
        self.save()

    def get_comment(self, id):
        comments = Comments.objects.filter(image_id =id)
        return comments

    def __str__(self):
        return self.comment
    
class Category(models.Model):
    photo_category = models.CharField(max_length=50)
    
    def save_category(self):
        self.save()
        
    def delete_category(self):
        self.delete()
    
    def update_category(self):
        self.update_category()
        
    @classmethod
    def get_category_id(cls, id):
        category = Category.objects.get(pk = id)
        return category

    def __str__(self):
        return self.photo_category
    
    
class Location(models.Model):
    image_location = models.CharField(max_length=50)
    
    @classmethod
    def get_all_locations(cls):
        all_locations = Location.objects.all()
        return all_locations
    
    def __str__(self):
        return self.image_location
    
class Subscriber(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    
class Review(models.Model):
    RATING_CHOICES = (
        (10, '10'),
        (20, '20'),
        (30, '30'),
        (40, '40'),
        (50, '50'),
        (60, '60'),
        (70, '70'),
        (80, '80'),
        (90, '90'),
        (100, '100'),

    )
    project = models.ForeignKey(Image, null=True, blank=True, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='reviews')
    ratings = models.IntegerField(choices=RATING_CHOICES, default=0)    
