from django.contrib import admin
import models

class LinkInline(admin.TabularInline):
    model = models.Link

class VoteInline(admin.TabularInline):
    model = models.Vote
    
class ReadingInline(admin.TabularInline):
    model = models.Reading

class BookAdmin(admin.ModelAdmin):
    inlines = [
        LinkInline,
        VoteInline,
        ReadingInline,
    ]

admin.site.register(models.Book, BookAdmin)