from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .models import Tweet
import random
from .forms import TweetForm
# Create your views here.

ALLOWED_HOST = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html",context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOST):
            return redirect(next_url)
        form = TweetForm()
    return render(request, "components/form.html", context={"form": form})

def tweet_list_view(request, *args, **kwargs):
    obj = Tweet.objects.all()
    tweet_list = [{"id": val.id, "content": val.content, "likes": random.randint(0,100)} for val in obj]
    data = {
        "isUsers": False, 
        "response": tweet_list,
        }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
        REST API
        Returns json data
    """
    data = {
        "id": tweet_id,        
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data["message"] = "Not found"
        status = 404

    return JsonResponse(data, status=status)