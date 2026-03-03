from django.urls import path
from .views import blogs_by_category

urlpatterns = [
    path('<int:category_id>/', blogs_by_category, name='blogs_by_category')
]
