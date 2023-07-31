from django.urls import path
from home import views


urlpatterns = [
    # BASIC VIEW -------------------------------------------------------------------------------------------------
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('fotos/', views.FotosView.as_view(), name='fotos'),
    path('nosotros/', views.NosotrosView.as_view(), name='nosotros'),

]
