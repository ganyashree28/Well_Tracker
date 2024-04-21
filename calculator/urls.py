# calculator/urls.py
# from django.urls import path
# from .views import calculate_body_fat

# urlpatterns = [
#     path('', calculate_body_fat, name='calculate'),
# ]

# calculator/urls.py

# from django.urls import path
# from .views import calculate_body_fat, page1  # Import the new home view and page1

# urlpatterns = [
#     path('', calculate_body_fat, name='calculate'),               # Path for the home page
#     path('page1/', page1, name='page1'),       # Path for the body fat calculator
#     # Add more paths for other pages as needed
# ]



# calculator/urls.py

from django.urls import path
from . import views
from .views import home, page1, water_intake_calculator, product_search, sleep_calculator, signup_view, login_view # Make sure these are the correct view function names

urlpatterns = [
    path('', home, name='home'),         # Assuming you have a 'home' view function
    path('page1/', page1, name='page1'), # Make sure 'page1' is the correct view function for body fat calculation
    # path('page2/', page2, name='page2'), # Uncomment this if you have a 'page2' view function
    path('water_intake/', water_intake_calculator, name='water_intake'),
    path('product_search/', product_search, name='product_search'),
    path('sleep_calculator/', sleep_calculator, name= 'sleep_calculator'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    
]




