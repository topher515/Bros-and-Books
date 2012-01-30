from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    author = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    pages = models.CharField(max_length=256)
    mode = models.CharField(max_length=16,
        choices=(
            ('reading','Reading'),('read','Read'),('reject','Rejected'),('upcoming','Upcoming'),('proposed','Proposed'),
            ),
        default='proposed'
        )
    
    def current_reading(self):
        return self.readings.order_by('-start_date')[0]
        
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
    
    def time_left(self):
        return (self.end_date - self.start_date)

class Vote(models.Model):
    book = models.ForeignKey(Book, related_name='votes')
    vote = models.IntegerField()
    user = models.ForeignKey(User,null=True)
    ts = models.DateTimeField()