from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

# Renders the index page
def index(request):
    return render(request, 'index.html')


# Displays a list of all tweets, ordered by creation date (most recent first)
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweet': tweets})


# Handles the creation of a new tweet
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})


# Deletes a specific tweet by ID if it belongs to the current user
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})
