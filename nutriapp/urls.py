from django.conf.urls import include,url
from .views import nutriView

urlpatterns=[
url(r'^nutriviewurl/?$',nutriView.as_view())
]