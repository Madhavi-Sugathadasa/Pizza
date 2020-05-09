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
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

 


