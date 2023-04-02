from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Tweet

MAX_TWEET_LENGTH = 240

class TweetForm(ModelForm):
    class Meta():
        model = Tweet
        fields = ['content']
        
        def clean_content(self):
            content = self.cleaned_data["content"]
            if len(content) > MAX_TWEET_LENGTH:
                raise ValidationError("This tweet is too long")
            return content
        