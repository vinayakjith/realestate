from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Property, User, Report, AdminAccount,Payment
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def adminhome(request):
    properties = Property.objects.all().filter(status='available').order_by('-updated_at')
    profile=Profile.objects.get(user=request.user)
    context={
        'properties':properties,
        'profile':profile
    }

    return render(request,'adminpanel/adminhome.html', context)
@login_required
def dashboard(request):
    users=User.objects.all()
    total_users=User.objects.count()
    total_postings=Property.objects.count()
    admin_account = AdminAccount.objects.first()
    payments=Payment.objects.all().order_by('-created_at')
    property=Property.objects.all().filter(status="notavailable").order_by('-created_at')
    profile=Profile.objects.get(user=request.user)
    print(admin_account.balance)
    context={
        'total_users':total_users,
        'total_postings':total_postings,
        'balance':admin_account.balance,
        "users":users,
        "payments":payments,
        "property":property,
        'profile':profile
    }
    return render(request,'adminpanel/dashboard.html',context)


@login_required
def property_reports(request):
    reports=Report.objects.all().order_by('-created_at')
    profile=Profile.objects.get(user=request.user)
    context={
        'reports':reports,
        'profile':profile
    }
    return render(request,'adminpanel/property_reports.html',context)
    
@login_required
def userstatus(request, user_id):
    user=get_object_or_404(User, id=user_id)
    if request.user!=user:
        user.is_active=not user.is_active
        user.save()
        return redirect('adminpanel:dashboard')
    
    print(user_id)

@login_required
def noprofile(request):
    return render(request,'adminpanel/noprofile.html')

@login_required
def transaction_history(request):
    payments=Payment.objects.all().order_by('-created_at')
    profile=Profile.objects.get(user=request.user)

        
    context={
        'payments':payments,
        'profile':profile

    }
    return render(request,'adminpanel/transaction_history.html',context)

@login_required
def listings(request):
    property=Property.objects.all().order_by('-created_at')

    context={
    'property':property
    }
    return render(request,'adminpanel/listings.html',context)
@login_required
def approve(request, property_id):
    property=get_object_or_404(Property, id=property_id)
    if property.status=='notavailable':
        property.status='available'
    context={
        'property':property,
        
    }

    property.save()
    return redirect('adminpanel:dashboard')
@login_required
def userlogout(request):
    logout(request)
    return redirect('sitevisitor:sitehome')
