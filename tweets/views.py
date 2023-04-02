from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from .models import Tweet
import random
from .forms import TweetForm
# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html",context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
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