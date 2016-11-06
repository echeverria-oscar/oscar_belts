from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages
import datetime
# Create your views here.
def index(request):

    return render(request, 'belt/index.html')

def register(request):

    if request.method == "POST":
       form_errors = User.objects.validate(request.POST)

    if len(form_errors) > 0:
       for error in form_errors:
           messages.error(request, error)
    else:
        User.objects.register(request.POST)
        messages.success(request, "You have successfully registered! Please login to continue")

    return redirect('/')

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Not login credentials!")
            return redirect('/')
        else:
           request.session['logged_user'] = user.id
           return redirect('/wishes')

def logout(request):
    if 'logged_user' in request.session:
        request.session.pop('logged_user')
    return redirect('/')


def wishes(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    me = User.objects.get(id=request.session['logged_user'])
    my_wishes = Wish.objects.filter(user=me) | Wish.objects.filter(wisher=me)
    others_wishes = Wish.objects.exclude(id__in=my_wishes)
    context = {
    "me" : me,
    'my_wishes': my_wishes,
    'others_wishes': others_wishes
    }

    return render(request, 'belt/wishes.html', context)

def addwish(request):
    if 'logged_user' not in request.session:
        return redirect('/')

    return render(request, 'belt/addwish.html')

def process_wish(request):
    user = User.objects.get(id=request.session['logged_user'])
    get_wish=request.POST['wish']
    print get_wish
    if request.POST:
        errors = Wish.objects.v_wish(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
                return redirect('/addwish')
        else:
            Wish.objects.create(wish=request.POST['wish'],user = user)

    return redirect('/wishes')

def view_wish(request, id):
    if 'logged_user' not in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=id)
    me = User.objects.get(id=request.session['logged_user'])

    wishers_added = User.objects.filter(other_wish=id)
    context = {
        'wish' : wish,
        'wishers_added': wishers_added
    }
    return render(request, 'belt/view_wish.html', context)

def join_wish(request, id):
    me = User.objects.get(id=request.session['logged_user'])
    wish = Wish.objects.get(id=id)
    wish.wisher.add(me)
    wish.save()
    return redirect('view_wish', id=wish.id)

def remove(request, id):
    wish = Wish.objects.get(id=id)
    user = User.objects.get(id=request.session['logged_user'])
    wish.wisher.remove(user)

    return redirect('view_wish', id=wish.id)

def delete(request, id):
    wish = Wish.objects.get(id=id)
    user = User.objects.get(id=request.session['logged_user'])
    wish.delete()

    return redirect("/wishes")
