from django.shortcuts import render
from django.http import HttpResponse
from .utils.calculator import Calcu
from .decorators import checkage_required



# Create your views here.
def home(request):
    context = {}
    return render(request, 'calculator/home.html')


def calu(request):
    # context = {}
    # return HttpResponse("Calculate solution")

    result = 0
    if request.method == 'POST':
        # request.GET.get("num1") # for GET REQUEST
        # request.GET.get("num2") # for GET REQUEST
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        # Note: if the above is empty or none, will throw an error
        opp = request.POST.get("opp")

        calcu = Calcu(num1, num2, opp)
    return render(request, 'calculator/home.html', {'result': calcu.calculate()})

@checkage_required
def check_age_page(request):
    return HttpResponse("Welcome! You are old enough to see this page.")