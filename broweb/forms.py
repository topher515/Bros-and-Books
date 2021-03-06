from django import forms
import models

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        exclude = ('mode',)
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        includes = ('book','text')