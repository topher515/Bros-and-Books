from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('broweb.views',
    url(r'^login-or-create/$', 'login_or_create', name="login"),
    url(r'^logout/$', 'logout', name="logout"),
    url(r'^books/(?P<book_id>\d+)/downvote/$', 'downvote', name="downvote"),
    url(r'^books/(?P<book_id>\d+)/upvote/$', 'upvote', name='upvote'),
    url(r'^$', 'index', name="index"),
)
