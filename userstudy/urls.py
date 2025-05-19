from django.conf.urls import url, include
from userstudy import views

urlpatterns = [
    url('^$',                   views.index,                name='index'),
    url(r'^main',               views.main,                 name='main'),
    url(r'^finish',             views.finish,               name='finish'),
    url(r'^dump',               views.dump,                 name='dump'),
]
