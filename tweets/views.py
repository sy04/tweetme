import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect

from .models import Tweet
from .forms import TweetForm

# Create your views here.
def home_page(request, *args, **kwargs):
  return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
  form = TweetForm(request.POST or None)
  next_url = request.POST.get("next") or None

  if form.is_valid():
    obj = form.save(commit=False)
    if next_url != None:
      return redirect(next_url)
    obj.save()
    form = TweetForm()

  return render(request, 'components/form.html', context={"form": form})

def tweet_list_view(request, *args, **kwargs):
  qs = Tweet.objects.all()
  tweet_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 500)} for x in qs]
  data = {
    "isUser": False,
    "response": tweet_list
  }

  return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
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
