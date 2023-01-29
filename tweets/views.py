import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_page(request, *args, **kwargs):
  return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST'])
def tweet_create_view(request, *args, **kwargs):
  serializer = TweetSerializer(data=request.POST or None)
  if serializer.is_valid(raise_exception=True):
    serializer.save(user=request.user)
    return Response(serializer.data, status=201)
  return Response({}, status=400)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
  qs = Tweet.objects.filter(id=tweet_id)
  if not qs.exists():
    return Response({}, status=404)
  obj = qs.first()
  serializer = TweetSerializer(obj)
  return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
  qs = Tweet.objects.all()
  serializer = TweetSerializer(qs, many=True)
  return Response(serializer.data, status=200)

def tweet_create_view_pure_django(request, *args, **kwargs):
  is_ajax = request.META.get('HTTP_X_REQUESTED_WITH' or 'X-Requested-With') == 'XMLHttpRequest'
  user = request.user

  if not request.user.is_authenticated:
    user = None
    if is_ajax:
      return JsonResponse({}, status=401)
    return redirect(settings.LONGIN_URL)

  form = TweetForm(request.POST or None)
  next_url = request.POST.get("next") or None

  if form.is_valid():
    obj = form.save(commit=False)
    obj.user = user
    obj.save()

    if is_ajax:
      return JsonResponse(obj.serialize(), status=201)

    if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
      return redirect(next_url)

    form = TweetForm()

  if form.errors:
    if is_ajax:
      return JsonResponse(form.errors, status=400)

  return render(request, 'components/form.html', context={"form": form})

def tweet_list_view_pure_django(request, *args, **kwargs):
  qs = Tweet.objects.all()
  tweet_list = [x.serialize() for x in qs]
  data = {
    "isUser": False,
    "response": tweet_list
  }

  return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
  data = {
    "id": tweet_id,
    # "content": obj.content,
    # "image_path": obj.image.url
  }

  status = 200

  try:
    obj = Tweet.objects.get(id=tweet_id)
    data['content'] = obj.content
  except:
    data['message'] = "Not Found"
    status = 404

  return JsonResponse(data, status=status)
