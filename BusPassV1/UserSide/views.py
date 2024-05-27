from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from AdminSide.models import *
from django.contrib import messages
import datetime
from django.http import HttpResponse,HttpResponseBadRequest, JsonResponse
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
# ------------------------------------ LOGIN,REGISTER,MASTER PAGE,INDEX PAGE,LOGOUT -----------------------------
def user_register(request):
    if request.method=="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        print("Username",username,"Email",email,"Password",password)
        
        u = User.objects.create_user(username=username,email=email,password=password)
        u.save()
        print("User created")
        return redirect(user_login)
    else:
        return render(request,"UserSide/user_register_page.html")

def user_login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]

        print("Username",username,"Password",password)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(user_index_page)
        else:
            return render(request,"UserSide/user_login_page.html")
    else:
        return render(request,"UserSide/user_login_page.html")

def user_master_page(request):
    return render(request,"UserSide/user_master_page.html")

def user_index_page(request):
    pass_prices = PassPrice.objects.all()
    three_month_pass_prices = PassPrice.objects.filter(pass_type=3)
    six_month_pass_prices = PassPrice.objects.filter(pass_type=6)
    return render(request,"UserSide/user_index_page.html",{
        "pass_prices":pass_prices,
        "three_month_pass_prices":three_month_pass_prices,
        "six_month_pass_prices":six_month_pass_prices})

def user_logout(request):
    logout(request)
    return redirect(user_index_page)

# ------------------------------ LOGIN,REGISTER,MASTER PAGE,INDEX PAGE ENDS HERE --------------------------------

# -------------------------------------- BUSES ROUTES,CHECK ROOT PASSES -----------------------------------------

def buses_routes(request):
    bus_routes = BusRoute.objects.all()
    return render(request,"UserSide/bus_routes.html",{"bus_routes":bus_routes})
 
def buses_routes_passes(request,pk):
    #selected_bus_route_passes = PassPrice.objects.filter(route_id=pk)
    #print("Selected bus route passes :- ", selected_bus_route_passes)
    
    selected_route_pass_details = PassPrice.objects.filter(route_id=pk)
    print("Selected route pass details :- ",selected_route_pass_details)

    three_month_bus_route_passes = PassPrice.objects.filter(route_id=pk,pass_type=3)
    print("Three month bus route passes :- ", three_month_bus_route_passes)

    six_month_bus_route_passes = PassPrice.objects.filter(route_id=pk,pass_type=6)
    print("Six month bus route passes :- ", six_month_bus_route_passes)

    return render(request,"UserSide/selected_bus_route_passes.html",{
        "selected_route_pass_details":selected_route_pass_details,
        "three_month_bus_route_passes":three_month_bus_route_passes,
        "six_month_bus_route_passes":six_month_bus_route_passes})
    """
    return HttpResponse(selected_bus_route_passes)
    """

# ---------------------------------- BUSES ROUTES,CHECK ROOT PASSES ENDS HERE -----------------------------------

# ---------------------------------- BUY PASSES,VIEW APPLICATIONS,REPORT ISSUES ---------------------------------

def buy_pass(request,pk):
    selected_pass = PassPrice.objects.get(id=pk)
    if request.method == "POST":
        userId = User.objects.get(id=request.user.id)
        passStartDate = request.POST["passstartdate"]
        passEndDate = request.POST["passenddate"]
        mobileNumber = request.POST["mobilenumber"]
        profileImage = request.FILES["profileimage"]
        documentId = request.FILES["documentimage"]

        # Convert the date string to a datetime object
        print(passStartDate,passEndDate)
        
        # Convert the date string to a datetime.date object
        convertedPassStartDate = datetime.datetime.strptime(passStartDate, '%Y-%m-%d').date()
        convertedPassEndDate = datetime.datetime.strptime(passEndDate, '%Y-%m-%d').date()
        print("Converted start date :- ", convertedPassStartDate, type(convertedPassStartDate))
        print("Converted end date :- ", convertedPassEndDate, type(convertedPassEndDate))

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(selected_pass.dis_price) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = PaymentDetails.objects.create(
            user=request.user.id, 
            amount=selected_pass.dis_price, 
            order_id=razorpay_order["id"]
        )
        order.save()
        
        pa = PassApplications()
        pa.pass_price_id = selected_pass
        pa.user_id = userId
        pa.mobile_number = mobileNumber
        pa.profile_image = profileImage
        pa.document = documentId
        pa.pass_start_date = str(convertedPassStartDate)
        pa.pass_end_date = str(convertedPassEndDate)
        pa.save()

        print("Pass Application :- ", pa.id)

        return render(
            request,
            "AdminSide/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/callback/",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
        """
        # Save the order details in the database
        payment = PaymentDetails(
            user=User.objects.get(id=request.user.id),
            pass_application=pa,
            order_id=order['id'],
            amount=amount / 100,
            currency=currency,
            payment_status='created'
        )
        payment.save()

        messages.success(request,"Pass application submitted.")
        return redirect(user_index_page)
        """
    else:
        return render(request,"UserSide/user_buy_pass.html",{"selected_pass":selected_pass})

def view_applied_applications(request):
    applied_passes = PassApplications.objects.filter(user_id=request.user.id)
    print("Applied passes :- ", applied_passes)
    return render(request,"UserSide/applied_applications.html",{"applied_passes":applied_passes})

def view_renewed_applications(request):
    renewed_applications = PassApplications.objects.filter(user_id=request.user.id,pass_status="2")
    return render(request,"UserSide/renewed_applications.html",{"renewed_applications":renewed_applications})

def report_issue(request):
    if request.method == "POST":
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]

        e = Enquiries()
        e.user_id = User.objects.get(id=request.user.id)
        e.email = email
        e.subject = subject
        e.message = message
        e.reply = ""
        e.save()

        messages.success(request,"Report Submitted to the admin,Please wait for the reply.")
        return redirect(report_issue)
    else:
        return render(request,"UserSide/report_enquiry.html")
    
def view_issues(request):
    issues_details = Enquiries.objects.all()
    return render(request,"UserSide/view_issues.html",{"issues_details":issues_details})

# ------------------------------- BUY PASSES,VIEW APPLICATIONS,REPORT ISSUES ENDS HERE --------------------------

# -------------------------------------------- RENEW PASS APPLICATION -------------------------------------------

def renew_pass(request,pk,status):
    selected_pass_to_renew = PassApplications.objects.get(id=pk)
    selected_pass_to_renew.pass_status = status
    selected_pass_to_renew.save()
    return redirect(view_renewed_applications)

# ---------------------------------------- RENEW PASS APPLICATION ENDS HERE -------------------------------------

# ---------------------------------------------- PAYMENT INERGRATION --------------------------------------------

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = PaymentDetails.objects.get(order_id=provider_order_id)
        order.payment_id = payment_id
        order.save()
        
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "AdminSide/callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "AdminSide/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "AdminSide/callback.html", context={"status": order.status})

# ----------------------------------------- PAYMENT INERGRATION ENDS HERE ---------------------------------------
