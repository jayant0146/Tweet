from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def fn(request):
    return render(request, "layout.html")

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_At')
    return render(request, "tweet_list.html", {"tweets": tweets})

@login_required
def tweet_create(request):
    if (request.method == "POST"): #user has sent the form after filling
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False) #commit false indicates don't save it to database
            tweet.user = request.user
            tweet.save() #Saved to database
            return redirect('tweet_list') #After saving redirected to another page        
    else: #If the form is empty or given to user
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

#While editing forms only instance = 'tweet' is new to provide the already filled form to edit
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

#deleting the form
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect("tweet_list")
    return render(request, "tweet_confirm_delete.html", {'tweet': tweet})

#whenever any func executes first whatever is there in return will be displayed on the screen then the further execution of the statement happens

#Decorators are just used to wrap the functions and to protect them from random users


#Custom User registration
# For registeration of the users, make the register folder in the outermost template folder, views, urls to be provided in the settings.py, urls.py
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form' : form})

# Cleaned_data is an object, not a function. A Form instance has an is_valid() method, which runs validation routines for all its fields. When this method is called, if all fields contain valid data, it will return True and place the form’s data in its cleaned_data attribute. So the cleaned_data is where to access the validated form data. form.is_valid() check all your validations against request.POST data and generate dictionary containing valid data which is form.cleaned_data. So data retrieved from forms.cleaned_data attribute are go through form validation. It's not only validation but also converted data to relevant python type too.

