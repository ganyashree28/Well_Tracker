
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm, CalculatorForm, WaterIntakeForm,ProductNameForm, SleepForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'calculator/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'calculator/login.html', {'form': form})





def home(request):
    
    return render(request, 'calculator/home.html')

def page1(request):
    # This function now represents your 'Page 1' where the calculator will be
    result = None
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            api_url = 'https://fu8odvcjmd.execute-api.eu-west-1.amazonaws.com/getBodyFatCal'
            params = {
                'weight': form.cleaned_data['weight'],
                'height': form.cleaned_data['height'],
                'age': form.cleaned_data['age'],
                'gender': form.cleaned_data['gender']
            }
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                result = response.json().get('BodyFatPercentage')
            else:
                result = f"Error: {response.json().get('message', 'Unknown error')}"
    else:
        form = CalculatorForm()
    
    return render(request, 'calculator/page1.html', {'form': form, 'result': result})



def water_intake_calculator(request):
    form = WaterIntakeForm(request.POST or None)
    recommended_water_intake = None  # Use this variable to pass the result to the template

    if request.method == 'POST' and form.is_valid():
        weight = form.cleaned_data.get('weight')
        activity_level = form.cleaned_data.get('activity_level')
        
  
        climate = form.cleaned_data.get('climate', 'moderate')  

        # Replace with your actual API endpoint
        api_endpoint = 'https://smvqlpky7g.execute-api.eu-west-1.amazonaws.com/test/helloworld?'

        # Prepare the data dictionary exactly how your API expects it
        data = {
            'weight': weight,
            'activity_level': activity_level,
            # Include 'climate' if it's needed by the API
            'climate': climate
        }

    
        try:
            response = requests.get(api_endpoint, json=data)  # Use json or data as needed
            if response.status_code == 200:
                # Adjust the key based on your API's response
                recommended_water_intake = response.json().get('recommended_water_intake_liters')
            else:
                # Log error details for debugging
                print(f"API Error {response.status_code}: {response.text}")
                recommended_water_intake = 'Failed to calculate. Please try again.'
        except requests.exceptions.RequestException as e:
            # Log the exception for debugging
            print(f"Request Exception: {e}")
            recommended_water_intake = 'Failed to calculate. Please try again.'

    return render(request, 'calculator/water_intake.html', {
        'form': form,
        'recommended_water_intake': recommended_water_intake
    })

def product_search(request):
    if request.method == 'GET' and 'product_name' in request.GET:
        form = ProductNameForm(request.GET)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            # Assuming Open Food Facts has a search endpoint that accepts product names
            response = requests.get(f'https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1')
            if response.ok:
                search_results = response.json().get('products', [])
                return render(request, 'calculator/product_search.html', {'products': search_results, 'form': form})
            else:
                error = 'Failed to retrieve product data.'
                return render(request, 'calculator/product_search.html', {'error': error, 'form': form})
    else:
        form = ProductNameForm()
    return render(request, 'calculator/product_search.html', {'form': form})















def sleep_calculator(request):
    context = {}
    form = SleepForm(request.POST or None)  # instantiate the form
    if request.method == 'POST' and form.is_valid():
        # Extracting hour and minute from the form
        hour = form.cleaned_data['hour']
        minute = form.cleaned_data['minute']
        meridiem = form.cleaned_data['meridiem']  # Ensure you have this field in your form

        # Convert to 24-hour format
        if meridiem == 'PM' and hour != 12:
            hour += 12
        elif meridiem == 'AM' and hour == 12:
            hour = 0

        # Assuming the user wants to wake up at this time
        desired_wakeup_time = timezone.localtime().replace(hour=hour, minute=minute, second=0, microsecond=0)

        # The time it takes on average to fall asleep
        fall_asleep_time = timedelta(minutes=14)

        # The website typically suggests 4-6 sleep cycles before the desired wake-up time
        sleep_cycle_duration = timedelta(minutes=90)  # Duration of one sleep cycle
        sleep_cycles = [4, 5, 6]  # Number of sleep cycles

        sleep_times = []  # This list will hold the calculated sleep times
        for cycle in sleep_cycles:
            sleep_time = desired_wakeup_time - (cycle * sleep_cycle_duration) - fall_asleep_time
            sleep_times.append(sleep_time.strftime("%I:%M %p"))

        # Pass the sleep times and the desired wake-up time to the context
        context['sleep_times'] = sleep_times
        context['desired_wakeup_time'] = desired_wakeup_time.strftime("%I:%M %p")

        # Render the sleep_times.html with the context containing sleep times
        return render(request, 'calculator/sleep_times.html', context)

    # If it's not a POST request or the form is not valid, include the form in the context
    context['form'] = form
    return render(request, 'calculator/sleep_form.html', context)




# def sleep_calculator(request):
#     if request.method == 'POST':
#         form = SleepForm(request.POST)
#         if form.is_valid():
#             hour = form.cleaned_data['hour']
#             minute = form.cleaned_data['minute']
#             bedtime = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            
#             wake_times = []
#             for cycle in [5, 6]:
#                 wake_time = bedtime + datetime.timedelta(minutes=90 * cycle)
#                 wake_times.append(wake_time.strftime("%Y-%m-%d %H:%M"))
            
#             return render(request, 'calculator/sleep_times.html', {'wake_times': wake_times, 'bedtime': bedtime.strftime("%Y-%m-%d %H:%M")})
#     else:
#         form = SleepForm()
    
#     return render(request, 'calculator/sleep_form.html', {'form': form})

























# def find_hospital_pharmacy(request):
#     if request.method == 'POST':
#         # Use the data provided by the user to get the location name
#         location_name = request.POST.get('location_name')
        
#         # First, convert the location name to latitude and longitude
#         geocoding_api_key = '81ea45a6e2b24a1196c90b7812ed68fa'  # Replace with your actual API key
#         geocoding_api_url = f'https://api.geoapify.com/v1/geocode/search?text=38%20Upper%20Montagu%20Street%2C%20Westminster%20W1H%201LJ%2C%20United%20Kingdom&apiKey=81ea45a6e2b24a1196c90b7812ed68fa'
        
#         geocoding_response = requests.get(geocoding_api_url)
        
#         if geocoding_response.status_code == 200:
#             geocoding_data = geocoding_response.json()
#             # Assuming the first result is the most relevant
#             latitude = geocoding_data['features'][0]['properties']['lat']
#             longitude = geocoding_data['features'][0]['properties']['lon']

#             # Now, use the latitude and longitude to find nearby hospitals and pharmacies
#             places_api_url = f'https://api.geoapify.com/v2/places?categories=commercial.supermarket&filter=rect%3A10.716463143326969%2C48.755151258420966%2C10.835314015356737%2C48.680903341613316&limit=20&apiKey=81ea45a6e2b24a1196c90b7812ed68fa'  # Adjust radius in meters and limit as needed
            
#             places_response = requests.get(places_api_url)

#             if places_response.status_code == 200:
#                 # Process the data and pass it to the template
#                 hospitals_pharmacies = places_response.json()
#                 return render(request, 'calculator/find_hospital_pharmacy.html', {'hospitals_pharmacies': hospitals_pharmacies})
#             else:
#                 # Handle errors for places API
#                 error_message = places_response.text
#                 return render(request, 'calculator/find_hospital_pharmacy.html', {'error_message': error_message})
#         else:
#             # Handle errors for geocoding API
#             error_message = geocoding_response.text
#             return render(request, 'calculator/find_hospital_pharmacy.html', {'error_message': error_message})

#     # GET request or initial visit
#     return render(request, 'calculator/find_hospital_pharmacy.html')


# def find_hospital_pharmacy(request):
#     if request.method == 'POST':
#         # Use the data provided by the user to make a request to the API
#         latitude = request.POST.get('latitude')
#         longitude = request.POST.get('longitude')
        
#         api_key = '81ea45a6e2b24a1196c90b7812ed68fa'  # Replace with your actual API key
#         api_url = 'https://maps.geoapify.com/v1/tile/carto/{z}/{x}/{y}.png?&apiKey=81ea45a6e2b24a1196c90b7812ed68fa'.format(latitude, longitude, api_key)
        
#         response = requests.get(api_url)
        
#         if response.status_code == 200:
#             # Process the data and pass it to the template
#             hospitals_pharmacies = response.json()
#             return render(request, 'find_hospital_pharmacy.html', {'hospitals_pharmacies': hospitals_pharmacies})
#         else:
#             # Handle errors
#             error_message = response.text
#             return render(request, 'find_hospital_pharmacy.html', {'error_message': error_message})

#     return render(request, 'calculator/find_hospital_pharmacy.html')

