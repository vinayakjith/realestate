from django.urls import path
from .views import sitehome

app_name = 'sitevisitor'
urlpatterns=[
    path('',sitehome,name='sitehome')
    
]