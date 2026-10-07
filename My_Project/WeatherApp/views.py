from django.shortcuts import render,redirect
from .forms import CityForm
from .models import City
import json
from urllib.parse import quote
from urllib.request import urlopen
from django.contrib import messages
from urllib.error import URLError,HTTPError


# Create your views here.
def home(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},&appid=24b26852121352634f05cd3f2e74b69b&units=metric'

    if(request.method == "POST"):

        form = CityForm(request.POST)

        if(form.is_valid()):

            Ncity = form.cleaned_data['name']

            Ccity = City.objects.filter(name=Ncity).count()

            if(Ccity == 0):

                res = json.loads(urlopen(url.format(quote(Ncity))).read())

                print(res)

                if(res['cod'] == 200 ):

                    form.save()

                    messages.success(request," " + Ncity + " Added Successfully...!!!")

                else:
                    messages.error(request," City Does Not Exists...!!!")
            else:
                messages.error(request," City Already Exists...!!!")

    form = CityForm()
    cities = City.objects.all()
    data = []
    for city in cities:
        try:

            response = urlopen(url)
            res = json.loads(response.read().decode('urf-8'))

            #Extract weather info
            city_weather = {
            'city'        :city.name,
            'temperature' : res['main']['temp'],
            'description' : res['weather'][0]['description'],
            'country'     : res['sys']['country'],
            'icon'        : res['weather'][0]['icon']
            }
            data.append(city_weather)

        except HTTPError as e:
            if(e.code == 404):
                messages.error(request,f"City'{city.name}'Not found in API")
            else:
                messages.error(request,f"API Error:{e.code}")

        except URLError as e:
            messages.error(request,f"Connection Error:{str(e)}")

        except json.JSONDecodeError:
            messages.error(request,f"Invaild response from API for {city.name}")

        except KeyError as e:
            messages.error(request,f"Missing field in API response:{str(e)}")

        except Exception as e:
            messages.error(request,f"Error fetchin weather:{str(e)}")

    context = {'data':data,'form':form}
    return render(request,"weatherapp_1.html",context)

from django.http import HttpResponse

def delete_city(request,city_id):
    try:
        city = City.objects.get( id = city_id)
        city_name = city.name
        city.delete()
        messages.success(request,f"'{city_name}'deleted!")
        
    except City.DoesNotExist:
        messages.error(request,"City not found")
    return redirect("Home")

