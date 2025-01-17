from django.urls import path
from .views import listings, userlogout,adminhome,property_reports,dashboard,userstatus, noprofile,transaction_history,approve
app_name='adminpanel'
urlpatterns=[
    path('',adminhome, name='adminhome'),
    path('property_reports/',property_reports,name='property_reports'),
    path('dashboard/',dashboard,name='dashboard'),
    path('userstatus/<int:user_id>/',userstatus,name='userstatus'),
    path('noprofile/',noprofile,name='noprofile'),
    path('transaction_history/',transaction_history,name='transaction_history'),
    path('approve/<int:property_id>/',approve,name='approve'),
    path('userlogout/',userlogout,name='userlogout'),
    path('listings/',listings,name='listings')






]