from django.urls import path
from . import views
 
urlpatterns = [ 
    path("admin-login-page",views.admin_login_page,name="admin-login-page"),
    path("admin-master-page",views.admin_master_page,name="admin-master-page"),
    path("admin-index-page",views.admin_index_page,name="admin-index-page"),
    path("admin-logout",views.admin_logout,name="admin-logout"),
    
    path("add-bus-route",views.add_bus_route,name="add-bus-route"), 
    path("buses-routes-details",views.buses_routes_details,name="buses-routes-details"),
    path("delete-buses-routes/<int:pk>",views.delete_buses_routes,name="delete-buses-routes"),
    path("update-buses-routes/<int:pk>",views.update_buses_routes,name="update-buses-routes"),
    
    path("add-buses-details",views.add_buses_details,name="add-buses-details"),
    path("show-buses-details",views.show_buses_details,name="show-buses-details"),
    path("delete-buses-details/<int:jk>",views.delete_buses_details,name="delete-buses-details"),
    path("update-buses-details/<int:jk>",views.update_buses_details,name="update-buses-details"),
 
    path("add-pass-price",views.add_pass_price,name="add-pass-price"),
    path('get-route-details/', views.get_route_details, name='get_route_details'),
    path("show-pass-price-details",views.show_pass_price_details,name="show-pass-price-details"),
    path("update-pass-price/<int:jk>",views.update_pass_price,name="update-pass-price"),
    path("delete-pass-price/<int:jk>",views.delete_pass_price,name="delete-pass-price"),

    path("buses-pass-application",views.buses_pass_application,name="buses-pass-application"),
    path("update-pass-status/<int:pk>/<int:status>",views.update_pass_status,name="update-pass-status"),

    path("view-users-issues",views.view_users_issues,name="view-users-issues"),
    path("update-issue-status/<int:pk>/<int:status>",views.update_issue_status,name="update-issue-status"),
    
]
