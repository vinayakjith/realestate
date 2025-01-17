from django.shortcuts import render
from adminpanel.models import Property
# Create your views here.

app_name='sitevisitor'
def sitehome(request):
    properties = Property.objects.all().filter(status='available').order_by('-updated_at')
    context={
        'properties':properties,

    }
    return render(request,'sitevisitor/sitehome.html',context)