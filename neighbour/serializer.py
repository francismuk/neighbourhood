from rest_framework import serializers
from .models import Image, Profile

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('name', 'description', 'price')
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('image', 'title', 'post' , 'poster', 'post_date', 'project_url','comments')