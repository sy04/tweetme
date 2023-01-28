from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet
# Create your views here.
def home_page(request, *args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")

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
