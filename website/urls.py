from django.urls import path

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data, name='data'),
    path('data/<int:datapoint_id>/', views.sample, name='sample'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('map/', views.map, name='map'),
]
