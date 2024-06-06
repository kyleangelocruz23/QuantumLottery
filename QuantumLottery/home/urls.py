from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
import os

urlpatterns = [
    path('', views.index, name='index'),
    path('check-results/', views.check_results, name='check_results'),
    path('check-results/<str:ticket_id>/', views.check_results, name='check_results_ticket_id'),
    path('generate-winning-numbers/', views.generate_winning_numbers, name='generate_winning_numbers'),
    path('reset-lottery/', views.reset_lottery, name='reset_lottery'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'home', 'static'))
