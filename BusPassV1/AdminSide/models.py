from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BusRoute(models.Model):
    route_id = models.CharField(max_length=200)
    route_start = models.CharField(max_length=200)
    route_end = models.CharField(max_length=200)
    distance = models.CharField(max_length=200)

    def __str__(self):
        return "Id :- {a} Route ID :- {b} Route Start :- {c} Route End :- {d}".format(a=self.id,b=self.route_id,c=self.route_start,d=self.route_end)

class Buses(models.Model):
    bus_name = models.CharField(max_length=200)
    bus_no = models.CharField(max_length=200)
    bus_registration_no = models.CharField(max_length=200)
    setting_capacity = models.CharField(max_length=200)
    standing_capacity = models.CharField(max_length=200)

class Drivers(models.Model):
    driver_name = models.CharField(max_length=200)
    driver_id = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=200)
    bus_no = models.ForeignKey(Buses,on_delete=models.CASCADE)
    duty_timing = models.CharField(max_length=200)
    driver_status = models.CharField(max_length=200)

class PassPrice(models.Model):
    route_id = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    dis_price = models.CharField(max_length=200)
    pass_type = models.CharField(max_length=20,default="")
    final_half_price = models.CharField(max_length=200,default="")
    pass_price_per_month = models.CharField(max_length=200,default="")

    def __str__(self):
        return "{a} Pass Price :- {b}".format(a=self.route_id,b=self.pass_type)

class PassApplications(models.Model):
    pass_price_id = models.ForeignKey(PassPrice,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    pass_start_date = models.CharField(max_length=200)
    pass_end_date = models.CharField(max_length=200)
    pass_status = models.CharField(max_length=50,default=0)
    create_date = models.DateField(auto_now_add=True)
    renew_date = models.CharField(max_length=200,default="")
    profile_image = models.ImageField(upload_to="pass_profile",default="")
    document = models.ImageField(upload_to="pass_document",default="")
    mobile_number = models.CharField(max_length=20,default="")

    class Meta:
        ordering = ['-create_date']  # Specify the default ordering for the model

    def __str__(self):
        return "Username :- {a} Pass Price :- {b} Pass Type :- {c}".format(a=self.user_id.username,b=self.pass_price_id,c=self.pass_price_id.pass_type)
    
class PaymentDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pass_application = models.ForeignKey(PassApplications, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    payment_status = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} for {self.user.username}"
    
class Enquiries(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=100,default="")
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=200)
    reply = models.CharField(max_length=200)
    status = models.CharField(max_length=50,default=0)

    def __str__(self):
        return "Username :- {a} Enquiry Subject :- {b} Status :- {c}".format(a=self.user_id.username,b=self.subject,c=self.status)
