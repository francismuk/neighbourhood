from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from .models import Subscriber, Image, Location, Category, Comments, Profile
from .forms import SubscribeForm, NewPostForm, CommentForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
import datetime as dt
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ImageSerializer, ProfileSerializer
from rest_framework import status


# Create your views here.

def index(request):
    title = 'Home'
    current_user = request.user

    
    images = Image.objects.all()
    if request.method == 'POST':   
        name = request.POST.get('your_name')
        email = request.POST.get('email')

        recipient = NewsLetterRecipients(name=name, email=email)
        recipient.save()
        send_welcome_email(name, email)
        data = {'success': 'You have been successfully added to mailing list'}
        return JsonResponse(data)

    else:
        form = SubscribeForm()

    return render(request, 'index.html', {'title': title, 'images': images, 'letterForm': form})

@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.poster = current_user
            image.save()
        return redirect('index')

    else:
        form = NewPostForm()
    return render(request, 'registration/new_post.html', {"form": form})

@login_required(login_url='/accounts/login/')
def search_projects(request):
    if 'image' in request.GET and request.GET["project"]:
        search_term = request.GET.get("image")
        searched_images = Image.search_images(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "projects": searched_projects})

    else:
        message = "You haven't searched for any person"
        return render(request, 'search.html', {"message": message})
    
def image(request, id):

    try:
        image = Image.objects.get(pk=id)

    except DoesNotExist:
        raise Http404()

    current_user = request.user
    comments = Comments.get_comment(Comments, id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']

            commentt = Comments()
            commentt.image = image
            commentt.user = current_user
            commentt.comment = comment
            commentt.save()

    else:
        form = CommentForm()

    return render(request, 'single.html', {"image": image,'form': form,'comments': comments})

class Projects(APIView):
    def get(self, request, format = None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many = True)
        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status= status.HTTP_201_CREATED)

        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
    
def newsletter(request):
    name = request.POST.get('your_name')
    email= request.POST.get('email')

    recipient= Subscriber(name= name, email =email)
    recipient.save()
    send_welcome_email(name, email)
    data= {'success': 'You have been successfully added to the newsletter mailing list'}
    return JsonResponse(data)