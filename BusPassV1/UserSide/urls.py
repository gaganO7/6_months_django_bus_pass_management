from django.urls import path
from . import views
 
urlpatterns = [ 
    path("user-register",views.user_register,name="user-register"),
    path("user-login",views.user_login,name="user-login"),
    path("user-master-page",views.user_master_page,name="user-master-page"),
    path("",views.user_index_page,name="user-index-page"),
    path("user-logout",views.user_logout,name="user-logout"),

    path("buses-routes",views.buses_routes,name="buses-routes"),
    path("bus-route-passes/<int:pk>",views.buses_routes_passes,name="bus-route-passes"),
    
    path("buy-pass/<int:pk>",views.buy_pass,name="buy-pass"),
    #path('payment-success/', views.payment_success, name='payment_success'),
    path("view-applied-applications",views.view_applied_applications,name="view-applied-applications"),
    path("view-renewed-applications",views.view_renewed_applications,name="view-renewed-applications"),
    path("renew-pass/<int:pk>/<int:status>",views.renew_pass,name="renew-pass"),
 
    path("report-issue",views.report_issue,name="report-issue"),
    path("view-issues",views.view_issues,name="view-issues"),

]
