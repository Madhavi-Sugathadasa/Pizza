from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("<int:menu_id>", views.item, name="item"),
    path("<int:menu_id>/add", views.add, name="add"),
    path("cart", views.shopping_cart, name="cart"),
    path("<int:cart_id>/remove", views.remove_item, name="remove"),
    path("order", views.order, name="order"),
    path("<int:order_id>/confirmation", views.confirmation, name="confirmation"),
    path("orders", views.orders, name="orders"),
    path("staff_login", views.staff_login_view, name="staff_login"),
    path("staff_orders", views.staff_orders_view, name="staff_orders"),
    path("<int:order_id>/staff_order_details", views.staff_order_details, name="staff_order_details"),
    path("<int:order_id>/change_status", views.change_status, name="change_status"),
    path("payment_success", views.payment_success, name="payment_success"),
    path("payment_cancel", views.payment_cancel, name="payment_cancel")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

 


