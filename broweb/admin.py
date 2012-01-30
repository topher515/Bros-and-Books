from django.contrib import admin
import models

class LinkInline(admin.TabularInline):
    model = models.Link

class VoteInline(admin.TabularInline):
    model = models.Vote

class BookAdmin(admin.ModelAdmin):
    inlines = [
        LinkInline,
        VoteInline,
    ]

admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Reading)