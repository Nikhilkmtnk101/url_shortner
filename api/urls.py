from django.urls import path
from .views import ShortnerListApiView,ShortnerCreateApiview,Redirector
urlpatterns = [
    path('list/',ShortnerListApiView.as_view(),name='all_links'),
    path('create/',ShortnerCreateApiview.as_view(),name='create_link'),
    path('<str:shortener_link>/',Redirector.as_view(),name='Redirector'),
]
