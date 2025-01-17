from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now
from django.utils import timezone
# Create your models here.

class AdminAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_account")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Admin Account - {self.user.username} - Balance: {self.balance}"

        
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image=models.ImageField(upload_to='profile_image/',default='profile_image/profile.png')
    user_bio=models.TextField(blank=True)
    phone=models.CharField(max_length=20)
    def average_rating(self):
        ratings = self.received_ratings.all()
        if ratings.exists():
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0

    def __str__(self):
        return self.user.username

class Property(models.Model):
    status_choices=[
        ('rent','Rent',),
        ('sale','Sale')
    ]

    property_status=[
        ('available','Available',),
        ('notavailable' ,'Not available'),
        ('sold','Sold')
    ]

    title=models.CharField(max_length=200)
    description=models.TextField()
    location=models.CharField(max_length=255)
    google = models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    property_type=models.CharField(max_length=20,choices=status_choices)
    status=models.CharField(max_length=15,choices=property_status,default='notavailable')
    images=models.ImageField(upload_to='property_images/')
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Report(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()  
    screenshot = models.ImageField(upload_to='screenshot/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.property.title} by {self.user.username}"
    
class OTP(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        expiration_time=self.created_at+timedelta(minutes=30)
        print(f"OTP Created At: {self.created_at}, Expiration Time: {expiration_time}, Current Time: {now()}")
        return now() <= expiration_time

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="wishlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')  # Prevents duplicate wishlist entries

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


class Rating(models.Model):
    reviewer=models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_ratings")
    agent=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_ratings")
    value=models.IntegerField()
    comment=models.TextField(blank=True)
    created_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('reviewer','agent')

    def __str__(self):
        return f"{self.reviewer.username} -> {self.agent.user.username}: {self.value}"
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id} - {'Success' if self.is_successful else 'Failed'}"


