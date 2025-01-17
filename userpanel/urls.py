from django.urls import path
from .views import error,payment_methods,clear_search,view_listings,userlogout,base,sold,userhome, register, userlogin, viewprofile, userprofile, viewposting,property,property_detail,changepass,forgot_password,validate_otp,reset_password,add_to_wishlist,remove_from_wishlist,view_wishlist,agent,rate_agent,editposting,deleteposting, qr_payment

app_name = 'userpanel'

urlpatterns = [
    path('', userhome, name='userhome'),
    path('register/', register, name='register'),
    path('userlogin/', userlogin, name='userlogin'),
    path('viewprofile/<int:user_id>/', viewprofile, name='viewprofile'),  
    path('userprofile/<int:user_id>/', userprofile, name='userprofile'),  
    path('viewposting/<int:property_id>/', viewposting, name='viewposting'),
    path('property/<int:user_id>/',property,name='property'),
    path('property_detail/<int:property_id>/',property_detail,name='property_detail'),
    path('changepass/',changepass,name='changepass'),
    path('sold/<int:property_id>/',sold,name='sold'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('validate_otp',validate_otp,name='validate_otp'),
    path('reset_password',reset_password,name='reset_password'),
    path('add_to_wishlist/<int:property_id>/',add_to_wishlist,name="add_to_wishlist"),
    path('remove_from_wishlist/<int:property_id>/',remove_from_wishlist,name='remove_from_wishlist'),
    path('view_wishlist/',view_wishlist,name='view_wishlist'),
    path('rate_agent/<int:agent_id>/',rate_agent,name="rate_agent"),
    path('agent/<int:agent_id>/',agent,name='agent'),
    path('base/',base,name='base'),
    path('editposting/<int:property_id>/',editposting,name='editposting'),
    path('deleteposting/<int:property_id>/',deleteposting,name='deleteposting'),
    path('userlogout/',userlogout,name='userlogout'),
    path('view_listings/',view_listings,name='view_listings'),
    path('clear_search/',clear_search,name='clear_search'),
    path('qr_payment/',qr_payment,name='qr_payment'),
    path('payment_methods/',payment_methods,name='payment_methods'),
    path('error/',error,name='error'),
    


]
