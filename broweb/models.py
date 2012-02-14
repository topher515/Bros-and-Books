import datetime
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    def get_upload_to(self,filename):
        return 'books/images/%s/%s' % (self.id,filename)
        
    author = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    pages = models.IntegerField()
    img = models.ImageField(upload_to=get_upload_to, null=True, blank=True)
    mode = models.CharField(max_length=16,
        choices=(
            ('reading','Reading'),('read','Read'),('reject','Rejected'),('upcoming','Upcoming'),('proposed','Proposed'),
            ),
        default='proposed'
        )
    
    def current_reading(self):
        return self.readings.order_by('-start_date')[0]
        
    def comments(self):
        return self.current_readings().comments
        
    def __str__(self):
        return '%s by %s' % (self.name,self.author)

    
class Link(models.Model):
    book = models.ForeignKey(Book, related_name='links')
    link = models.URLField(max_length=500)
    name = models.CharField(max_length=64,choices=(('amazon','Amazon.com'),('blank','(blank)')),default="blank")
    
class Reading(models.Model):
    book = models.ForeignKey(Book, related_name='readings')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def __str__(self):
        return ('Reading %s from %s until %s' % (self.book,self.start_date,self.end_date))
    
    def time_left(self):
        return (self.end_date - datetime.datetime.now())

    def pages_per_day(self):
        return self.book.pages / self.time_left().days
        
    def day_num(self):
        return (datetime.datetime.now()-self.start_date).days
        
    def through_pages(self):
        return self.day_num() * self.pages_per_day()
        
    def left_pages(self):
        return self.book.pages - self.through_pages ()


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name="comments")
    text = models.TextField()
    ts = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True,auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments")
    
class Vote(models.Model):
    book = models.ForeignKey(Book, related_name='votes')
    vote = models.IntegerField()
    user = models.ForeignKey(User,null=True)
    ts = models.DateTimeField()