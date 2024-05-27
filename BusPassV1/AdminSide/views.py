from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib import messages
from .models import *

# Create your views here.
# ----------------------------------- LOGIN, LOGOUT AND REGISTER -------------------------------------
def admin_login_page(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                messages.success(request,"Login Successfull.")
                return redirect(admin_index_page)
            else:
                messages.warning(request,"You are not authorized to access this panel.")
                return redirect(admin_login_page)
        else:
            messages.success(request,"Worng username or password.")
            return redirect(admin_login_page)
    else:
        return render(request,"AdminSide/admin_login_page.html")

def admin_master_page(request):
    return render(request,"AdminSide/admin_master_page.html")

def admin_index_page(request):
    total_routes = BusRoute.objects.all().count()
    total_pass_applications = PassApplications.objects.all().count()
    total_renew_pass_applications = PassApplications.objects.all().count()
    total_enquiries = Enquiries.objects.all().count()
    recent_pass_applications = PassApplications.objects.all().order_by("-create_date")[:10]
    return render(request,"AdminSide/admin_index_page.html",{
        "total_routes":total_routes,
        "total_pass_applications":total_pass_applications,
        "total_renew_pass_applications":total_renew_pass_applications,
        "total_enquiries":total_enquiries,
        "recent_pass_applications":recent_pass_applications
        })

def admin_logout(request):
    logout(request)
    messages.success(request,"Logout Successfull.")
    return redirect(admin_login_page)

# --------------------------------- LOGIN, LOGOUT AND REGISTER ENDS HERE ------------------------------

# ------------------------------------- Bus Route CRUD ------------------------------------------------

def add_bus_route(request):
    if request.method == "POST":
        routeID = request.POST["routeid"]
        routeStart = request.POST["routestart"]
        routeEnd = request.POST["routeend"]
        routeDistance = request.POST["distance"]

        existing_bus_route = BusRoute.objects.filter(route_id=routeID).exists()
        print("Existing route id :- ",existing_bus_route)
        if existing_bus_route:
            messages.warning(request,"Bus route already exist.")
            return redirect(add_bus_route)
        else:
            br = BusRoute()
            br.route_id = routeID
            br.route_start = routeStart
            br.route_end = routeEnd
            br.distance = routeDistance
            br.save()

            messages.success(request,"Bus route added successfully.")
            return redirect(buses_routes_details)
    else:
        return render(request,"AdminSide/add_bus_route.html")

def buses_routes_details(request):
    busses_routes = BusRoute.objects.all()
    return render(request,"AdminSide/show_buses_routes_details.html",{"busses_routes":busses_routes})

def delete_buses_routes(request,pk):
    selected_bus_route = BusRoute.objects.get(id=pk)
    selected_bus_route.delete()
    messages.success(request,"Bus route delete successfully.")
    return redirect(buses_routes_details)

def update_buses_routes(request,pk):
    selected_bus_route = BusRoute.objects.get(id=pk)
    if request.method == "POST":
        routeID = request.POST["routeid"]
        routeStart = request.POST["routestart"]
        routeEnd = request.POST["routeend"]
        routeDistance = request.POST["distance"]

        existing_bus_route = BusRoute.objects.filter(route_id=routeID).exists()
        print("Existing route id :- ",existing_bus_route)
        if existing_bus_route:
            messages.warning(request,"Bus route already exist.")
            return render(request,"AdminSide/update_bus_route.html",{"selected_bus_route":selected_bus_route})
        else:
            selected_bus_route.route_id = routeID
            selected_bus_route.route_start = routeStart
            selected_bus_route.route_end = routeEnd
            selected_bus_route.distance = routeDistance
            selected_bus_route.save()
        
            messages.success(request,"Bus route updated successfully.")
            return redirect(buses_routes_details)
    else:
        return render(request,"AdminSide/update_bus_route.html",{"selected_bus_route":selected_bus_route})

# -------------------------------------------- Bus Route CRUD Ends -------------------------------------

# -------------------------------------------- Buses Details CRUD --------------------------------------

def add_buses_details(request):
    if request.method == "POST":
        busName = request.POST["busname"]
        busNo = request.POST["busno"]
        busRegistrationNo = request.POST["busregistrationno"]
        settingCapacity = request.POST["settingcapacity"]
        standingCapacity = request.POST["standingcapacity"]

        existing_bus_details = Buses.objects.filter(bus_no=busNo).exists()
        print("Existing bus details :- ",existing_bus_details)
        if existing_bus_details:
            messages.warning(request,"Bus details already exist.")
            return redirect(add_buses_details)
        else:
            abr = Buses()
            abr.bus_name = busName
            abr.bus_no = busNo
            abr.bus_registration_no = busRegistrationNo
            abr.setting_capacity = settingCapacity
            abr.standing_capacity = standingCapacity
            abr.save()

            messages.success(request,"Buses details added successfully.")
            return redirect(show_buses_details)
    else:
        return render(request,"AdminSide/add_buses_details.html")

def show_buses_details(request):
    busses_details = Buses.objects.all()
    return render(request,"AdminSide/show_buses_details.html",{"busses_details":busses_details})

def delete_buses_details(request,jk):
    selected_route_details = Buses.objects.get(id=jk)
    selected_route_details.delete()
    messages.success(request,"Buses details deleted successfully.")
    return redirect(show_buses_details)

def update_buses_details(request,jk):
    selected_route_details = Buses.objects.get(id=jk)
    if request.method == "POST":
        busName = request.POST["busname"]
        busNo = request.POST["busno"]
        busRegistrationNo = request.POST["busregistrationno"]
        settingCapacity = request.POST["settingcapacity"]
        standingCapacity = request.POST["standingcapacity"]

        existing_bus_details = Buses.objects.filter(bus_no=busNo).exists()
        print("Existing bus details :- ",existing_bus_details)
        if existing_bus_details:
            messages.warning(request,"Bus details already exist.")
            return render(request,"AdminSide/update_buses_details.html",{"selected_route_details":selected_route_details})
        else:
            selected_route_details.bus_name = busName
            selected_route_details.bus_no = busNo
            selected_route_details.bus_registration_no = busRegistrationNo
            selected_route_details.setting_capacity = settingCapacity
            selected_route_details.standing_capacity = standingCapacity
            selected_route_details.save()

            messages.success(request,"Buses details updated successfully.")
            return redirect(show_buses_details)
    else:
        return render(request,"AdminSide/update_buses_details.html",{"selected_route_details":selected_route_details})

# --------------------------------------------- Buses Details CRUD Ends ---------------------------------

# ------------------------------------------------- Pass Price CRUD -------------------------------------

def add_pass_price(request):
    passes_details = BusRoute.objects.all()
    if request.method == "POST":
        routeID = request.POST["routeid"]
        passType = request.POST["passtypeId"]
        totalPrice = request.POST["totalPrice"]
        halfPrice = request.POST["finalPassPrice"]
        passPricePerMonth = request.POST["passpricepermonth"]

        existing_pass_price = PassPrice.objects.filter(route_id=BusRoute.objects.get(id=routeID)).exists()
        print("Existing pass price :- ",existing_pass_price)
        if existing_pass_price:
            messages.warning(request,"Pass price details already exist.")
            return render(request,"AdminSide/add_pass_price.html",{"passes_details":passes_details})
        else:
            pp = PassPrice()
            pp.route_id = BusRoute.objects.get(id=routeID)
            pp.dis_price = totalPrice
            pp.pass_type = passType
            pp.final_half_price = halfPrice
            pp.pass_price_per_month = passPricePerMonth
            pp.save()

            messages.success(request,"Pass price added successfully.")
            return redirect(show_pass_price_details)
    else:
        return render(request,"AdminSide/add_pass_price.html",{"passes_details":passes_details})

def get_route_details(request):
    route_id = request.GET.get('route_id')
    print("Selected route id :- ", route_id)
    bus_route = get_object_or_404(BusRoute, id=route_id)
    print("Bus route details :- ", bus_route)
    data = {
        'route_start': bus_route.route_start,
        'route_end': bus_route.route_end,
    }
    print("Returning json data :- ", data)
    return JsonResponse(data)
    
def show_pass_price_details(request):
    price_details = PassPrice.objects.all()
    return render(request,"AdminSide/show_pass_price_details.html",{"price_details":price_details})

def update_pass_price(request,jk):
    selected_pass_price = PassPrice.objects.get(id=jk)
    buses_routes = BusRoute.objects.all()
    selected_bus_route = get_object_or_404(BusRoute,id=selected_pass_price.route_id.id)
    
    if request.method == "POST":
        routeID = request.POST["routeid"]
        passType = request.POST["passtypeId"]
        totalPrice = request.POST["totalPrice"]
        halfPrice = request.POST["finalPassPrice"]
        passPricePerMonth = request.POST["passpricepermonth"]

        selected_pass_price.route_id = BusRoute.objects.get(id=routeID)
        selected_pass_price.dis_price = totalPrice
        selected_pass_price.pass_type = passType
        selected_pass_price.final_half_price = halfPrice
        selected_pass_price.pass_price_per_month = passPricePerMonth
        selected_pass_price.save()

        messages.success(request,"Pass price details updated successfully.")
        return redirect(show_pass_price_details)
    else:
        return render(request,"AdminSide/update_pass_price.html",{
            "selected_pass_price":selected_pass_price,
            "buses_routes":buses_routes,
            "selected_bus_route":selected_bus_route})

def delete_pass_price(request,jk):
    selected_pass_price = PassPrice.objects.get(id=jk)
    selected_pass_price.delete()
    messages.success(request,"Pass price details deleted successfully.")
    return redirect(show_pass_price_details)

# ----------------------------------------------- Pass Price CRUD Ends ----------------------------------

# ----------------------------------------------- BUS PASS APPLICATIONS ---------------------------------

def buses_pass_application(request):
    new_pass_applications = PassApplications.objects.all()
    if request.method=="POST":
        if request.POST.get("choose") is not None:
            print("Selected value :- ", request.POST.get("choose"))
            if request.POST.get("choose") == "0" or request.POST.get("choose") == "1" or request.POST.get("choose") == "2":
                new_pass_applications = PassApplications.objects.filter(pass_status=request.POST["choose"])
                print("Filtered pass applications :- ", new_pass_applications)
                return render(request,"AdminSide/buses_pass_application.html",{"new_pass_applications":new_pass_applications})
            else:
                return render(request,"AdminSide/buses_pass_application.html",{"new_pass_applications":new_pass_applications})
        else:
            print("Pass Applications :- ", new_pass_applications)
            return render(request,"AdminSide/buses_pass_application.html",{"new_pass_applications":new_pass_applications})
    else:
        return render(request,"AdminSide/buses_pass_application.html",{"new_pass_applications":new_pass_applications})
     
def update_pass_status(request,pk,status):
    selected_pass_application_details = PassApplications.objects.get(id=pk)
    print("Selected pass status :- ", selected_pass_application_details.pass_status)
    if selected_pass_application_details.pass_status == "0": # Pending
        selected_pass_application_details.pass_status = "1"
        selected_pass_application_details.save()
        return redirect(buses_pass_application)
    elif selected_pass_application_details.pass_status == "3": # For Renewed
        selected_pass_application_details.pass_status = "1"
        selected_pass_application_details.save()
        return redirect(buses_pass_application)
    else:
        return redirect(buses_pass_application)

# ------------------------------------------- BUS PASS APPLICATIONS ENDS HERE ---------------------------

# --------------------------------------------------- USERS ENQUIRIES -----------------------------------

def view_users_issues(request):
    issues_list = Enquiries.objects.all()
    if request.method=="POST":
        if request.POST.get("choose") is not None:
            print("Selected value :- ", request.POST.get("choose"))
            if request.POST.get("choose") == "0" or request.POST.get("choose") == "1":
                issues_list = Enquiries.objects.filter(status=request.POST["choose"])
                print("Filtered users enquiries :- ", issues_list)
                return render(request,"AdminSide/users_issues.html",{"issues_list":issues_list})
            else:
                return render(request,"AdminSide/users_issues.html",{"issues_list":issues_list})
        else:
            print("Users Issues :- ", issues_list)
            return render(request,"AdminSide/users_issues.html",{"issues_list":issues_list})
    else:
        return render(request,"AdminSide/users_issues.html",{"issues_list":issues_list})

def update_issue_status(request,pk,status):
    selected_user_issue = Enquiries.objects.get(id=pk)
    if request.method=="POST":
        reply = request.POST["reply"]

        selected_user_issue.reply = reply
        selected_user_issue.status = status
        selected_user_issue.save()
        
        messages.success(request,"User issue is resolved.")
        return redirect(view_users_issues)
    else:
        return render(request,"AdminSide/update_user_issue_status.html",{"selected_user_issue":selected_user_issue})

# ----------------------------------------------- USERS ENQUIRIES ENDS HERE -----------------------------




