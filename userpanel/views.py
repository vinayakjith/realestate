from django.shortcuts import render,redirect,get_object_or_404
from adminpanel.models import Property,Profile,User,OTP,Wishlist,Rating,Payment,AdminAccount
from .forms import RegistrationForm,ProfileForm,LoginForm,PropertyForm,ReportForm,Changepassword, Ratingform, Paymentform
from django.contrib.auth import authenticate,login,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .utils import generate_otp
from .tasks import send_otp_mail
from uuid import uuid4
from django.http import HttpResponseForbidden
from decimal import Decimal


@login_required
def userhome(request):
    properties = Property.objects.all().filter(status='available').order_by('-updated_at')
    

    # Handle missing Profile gracefully
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Redirect to profile creation page if no Profile exists
        messages.info(request,'You must complete your profile before logging in')
        return redirect('userpanel:userprofile', user_id=request.user.id)
    
    # Proceed to render the home page if Profile exists
    context = {
        'properties': properties,
        'profile': profile,
    }
    return render(request, 'userpanel/userhome.html', context)

def view_listings(request):
    properties = Property.objects.all().filter(status='available').order_by('-updated_at')
    profile=Profile.objects.get(user=request.user)
    category=request.GET.get('category', '').lower()
    location=request.GET.get('location', '')

    if category:
        properties=properties.filter(property_type__iexact=category)
    
    if location:
        properties=properties.filter(location__icontains=location)
    context={
        'properties':properties,
        'profile':profile
    }
    return render(request,'userpanel/viewlistings.html',context)

def clear_search(request):
    properties=Property.objects.all().order_by('-created_at')
    profile=Profile.objects.get(user=request.user)
    context={
        'properties':properties,
        'profile':profile
    }
    return render(request,'userpanel/viewlistings.html',context)
def base(request):
    user=request.user
    profile=user.profile
    context={
        'profile':profile,
        'user':user


    }
    return render(request,'userpanel/userbase.html',context)



def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User Registered Succesfully')




            return redirect('sitevisitor:sitehome')
    else:
        form=RegistrationForm()
    context={
        'form':form
    }
    return render(request,'userpanel/register.html',context)


def userlogin(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                if user.is_staff:
                    return redirect('adminpanel:adminhome')
                else:
                    return redirect('userpanel:userhome')
    else:
        form=LoginForm()
    context={
        'form':form,
        'user':request.user
    }

    return render(request,'userpanel/login.html',context)

@login_required
def viewprofile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user) 



    context = {
        'profile': profile,
        'user': user
    }

    return render(request, 'userpanel/viewprofile.html', context)

@login_required
def viewposting(request,property_id):
    property=get_object_or_404(Property, id=property_id)
    profile=Profile.objects.get(user=request.user)
    is_wishlisted = Wishlist.objects.filter(user=request.user, property=property).exists()
    agent = property.posted_by.profile
    # property = Property.objects.get(id=6)  # Replace with the property ID
    print(property.posted_by)  # Check the associated user
    print(property.posted_by.profile.id)  # Check the agent's profile ID
    print(f"Agent ID: {agent.id}")
    print(property.google)

    # profile=property.posted_by.profile
    context={
        'property':property,
        'is_wishlisted':is_wishlisted,
        'agent':agent,
        'profile':profile
    }
    return render(request,'userpanel/viewposting.html',context)


@login_required
def userprofile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.filter(user=user).first()
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request,'Profile added successfuly')
            return redirect('userpanel:userhome')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile':profile
    }
    return render(request, 'userpanel/userprofile.html', context)


@login_required
def property(request, user_id):
    user=get_object_or_404(User, id=user_id)
    profile=Profile.objects.get(user=request.user)
 
    if request.method=='POST':
        form=PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            
            property=form.save(commit=False)
            property.posted_by=request.user
            property.save()
            property.status='notavailable'
            messages.success(request,'Posting will be added once admin approves it')
            return redirect('userpanel:userhome')
        
    else:
        form=PropertyForm()
    
    context={
        'form':form,
        'user':user,
        'profile':profile
    }
    return render(request,'userpanel/property.html',context)

@login_required
def editposting(request, property_id):
    property=get_object_or_404(Property, id=property_id)
    user=request.user
    profile=Profile.objects.get(user=request.user)

    if property.posted_by==request.user:
        if request.method=='POST':
            form=PropertyForm(request.POST,request.FILES, instance=property)
            if form.is_valid():
                form.save()
                messages.success(request,'Posting edited succesully')
                return redirect('userpanel:viewposting', property_id=property.id)
        else:
            form=PropertyForm(instance=property)
    context={
        'form':form,
        'profile':profile
    }
    return render(request,'userpanel/editposting.html',context)


@login_required
def deleteposting(request, property_id):
    property=get_object_or_404(Property, id=property_id)
    user=request.user
    if property.posted_by==request.user:
        property.delete()
        messages.success(request,'Posting deleted succesfully')
        return redirect('userpanel:userhome')

@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    profile = None

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    report_form = ReportForm()
    if request.method == 'POST' and request.user.is_authenticated:
        report_form = ReportForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.property = property
            report.user = request.user
            report.save()
            print(request.POST)  # Debugging: Check POST data
            print(request.FILES)  # Debugging: Check file uploads
            print("Report saved successfully!")  # Debugging: Confirm save
            return redirect('userpanel:property_detail', property_id=property.id)
        else:
            print("Form is invalid:", report_form.errors)  # Debugging: Print form errors

    context = {
        'property': property,
        'report_form': report_form,
        'profile': profile,
    }
    return render(request, 'userpanel/property_detail.html', context)  # Always return HttpResponse



@login_required
def changepass(request):
    profile=Profile.objects.get(user=request.user)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Changepassword(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  
                messages.success(request, 'Change Password successful')
                return redirect('userpanel:userlogin')
        else:
            form = Changepassword(request.user)
    else:
        messages.success(request,"Please login")
        return redirect('userpanel:userlogin')

    context = {
        'form': form,
        'profile':profile
    }
    return render(request,'userpanel/changepass.html',context)

@login_required
def sold(request, property_id):
    property=get_object_or_404(Property, id=property_id)
    user=request.user
    if property.status=="available":
        property.status="notavailable"
        messages.success(request,"Property marked as Not available")
    else:
        property.status="available"
        messages.success(request,"Property marked as available")
    property.save()
    return redirect('userpanel:userhome')
    
def forgot_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        try:
            user=User.objects.filter(email=email).first()
            otp=generate_otp()
            OTP.objects.update_or_create(user=user, defaults={'otp':otp})
            send_otp_mail.delay(email,otp)
            messages.success(request,"OTP send to your mail")
            return redirect('userpanel:validate_otp')
        except User.DoesNotExist:
            messages.error(request,'No user found')
    return render(request,"userpanel/forgot_password.html")


def validate_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "No account found with this email.")
            return render(request, 'userpanel/validate_otp.html')

        if users.count() > 1:
            messages.error(request, "Multiple accounts found with this email. Please contact support.")
            return render(request, 'userpanel/validate_otp.html')
        user = users.first()

        try:
            otp_record = OTP.objects.get(user=user, otp=otp)

            if otp_record.is_valid():
                messages.success(request, "OTP validated. You can now reset your password.")
                return redirect('userpanel:reset_password')
            else:
                messages.error(request, "OTP has expired.")
        except OTP.DoesNotExist:
            messages.error(request, "Invalid OTP.")



    
    return render(request, 'userpanel/validate_otp.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully.")
            return redirect('userpanel:userlogin') 
        except User.DoesNotExist:
            messages.error(request, "An error occurred while resetting the password.")
    return render(request, 'userpanel/reset_password.html')

@login_required
def add_to_wishlist(request, property_id):
    property=get_object_or_404(Property, id=property_id)
    wishlist, created=Wishlist.objects.get_or_create(user=request.user, property=property)
    if created:
        messages.success(request,"Property added to you wishlist")
    else:
        messages.info(request,"This property is already in your wishlist")
    return redirect('userpanel:viewposting', property_id=property.id)

@login_required
def remove_from_wishlist(request, property_id):
    property=get_object_or_404(Property, id=property_id)
    wishlist=Wishlist.objects.filter(user=request.user, property=property)

    if wishlist.exists():
        wishlist.delete()
        messages.success(request,"This property removed from wishlist")
    else:
        messages.info(request,'This property is not in your wishlist')
    return redirect('userpanel:viewposting',property_id=property.id)

@login_required
def view_wishlist(request):
    profile=Profile.objects.get(user=request.user)
    wishlist_items=Wishlist.objects.filter(user=request.user).select_related('property')
    context={
        'wishlist_items':wishlist_items,
        'profile':profile
    }
    return render(request,"userpanel/view_wishlist.html",context)

@login_required
def rate_agent(request, agent_id):
    agent=get_object_or_404(Profile, id=agent_id)
    profile=Profile.objects.get(user=request.user)
    if request.method=='POST':
        form=Ratingform(request.POST)
        if form.is_valid():
            existing_rating=Rating.objects.filter(reviewer=request.user, agent=agent).first()
            if existing_rating:
                messages.error(request,"You have already rated this user")
                return redirect('userpanel:agent', agent_id=agent.id)
        rating=form.save(commit=False)
        rating.reviewer=request.user
        rating.agent=agent
        rating.save()
        messages.success(request,'Your rating have been submitted')
        return redirect('userpanel:agent', agent_id=agent.id)
    else:
        form=Ratingform()
    context={
        'form':form,
        'agent':agent,
        'profile':profile
    }
    return render(request,'userpanel/rate_agent.html',context)

@login_required
def agent(request, agent_id):
    agent=get_object_or_404(Profile,id=agent_id)
    ratings=agent.received_ratings.all()
    profile=Profile.objects.get(user=request.user)

    context={
        'agent':agent,
        'ratings':ratings,
        'profile':profile
    }
    return render(request,"userpanel/agent.html",context)

@login_required
def qr_payment(request):
    user_profile = request.user.profile
    profile=Profile.objects.get(user=request.user)

    if request.method == "POST":
        # Simulate a payment process
        transaction_id = str(uuid4())  # Generate unique transaction ID
        print(transaction_id)
        payment = Payment.objects.create(
            user=request.user,
            amount=100.00,
            transaction_id=transaction_id,
            is_successful=True  # Simulate successful payment
        )

        # Mark the profile as paid
        user_profile.has_paid = True
        user_profile.save()

        # Update admin balance
        admin_account, created = AdminAccount.objects.get_or_create(user=User.objects.filter(is_superuser=True).first())
        admin_account.balance += Decimal('100.00')
        admin_account.save()
        print(f"Admin Balance Before: {admin_account.balance}")
        print(f"Admin Balance After: {admin_account.balance}")


        messages.success(request, "Payment successful! You can now post your property.")
        return redirect('userpanel:property', user_id=  request.user.id)

    context={
        'profile':profile
    }

    return render(request, "userpanel/qr_payment.html",context)


@login_required(login_url='userpanel:userlogin')
def userlogout(request):
    logout(request)
    return redirect('sitevisitor:sitehome')

@login_required
def payment_methods(request):
    profile=Profile.objects.get(user=request.user)
    context={
        'profile':profile
    }
    return render(request,'userpanel/payment_methods.html',context)

@login_required
def error(request):
    profile=Profile.objects.get(user=request.user)
    context={
        'profile':profile
    }
    return render(request,'userpanel/error.html',context)
