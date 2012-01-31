import datetime
import json
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as dlogout
from django.contrib import messages

from models import Book, Vote

def index(request):
    now = datetime.datetime.now()
    current_books = Book.objects.filter(mode='reading',readings__end_date__gt=now).select_related('readings')
    proposed = Book.objects.filter(mode='proposed').annotate(sum_votes=Sum('votes__vote'),count_votes=Count('votes'))
    context = {
        'current_books':current_books,
        'proposed':proposed,
    }
    return render_to_response('broweb/index.html',RequestContext(request,context))

def login_or_create(request):
    username = request.REQUEST.get('username')
    password = request.REQUEST.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        user = User.objects.create_user(username,email='',password=password)
        user = authenticate(username=username, password=password)
        login(request,user)
        messages.warning(request,'Hi %s, we created a new account for you!' % username)
    else:
        login(request,user)
        messages.success(request,'Hi %s, you were successfully logged in.' % username)
    
    return redirect(request.META.get('HTTP_REFERER'),'/')
   
def logout(request):
    dlogout(request)
    messages.success(request,'You\'ve been logged out.' % username)
    return redirect(request.META.get('HTTP_REFERER'),'/')
    
def ok_to_vote(request,book_id):
    if not request.session.get('votes'):
        request.session['votes'] = {}
    voted = request.session['votes'].get(int(book_id))
    if voted is not None and datetime.datetime.now() <= voted + datetime.timedelta(hours=1):
        return False
    else:
        request.session['votes'][int(book_id)] = datetime.datetime.now()
        request.session.modified = True
        return True

def downvote(request,book_id):
    book = get_object_or_404(Book,id=book_id)
    if not ok_to_vote(request,book_id):
        return HttpResponse(json.dumps({'message':'You can only vote once an hour.'}),status=403)
    now = datetime.datetime.now()
    vote = Vote(book=book,ts=now,vote=-1, user=request.user).save()
    return HttpResponse(status=200)
    
def upvote(request,book_id):
    book = get_object_or_404(Book,id=book_id)
    if not ok_to_vote(request,book_id):
        return HttpResponse(json.dumps({'message':'You can only vote once an hour.'}),status=403)
    now = datetime.datetime.now()
    vote = Vote(book=book,ts=now,vote=1, user=request.user).save()
    return HttpResponse(status=200)

    