from django.shortcuts import render
#----custom start here-----
#from django.http import HttpResponse
from generator import generate, resolve
from django.shortcuts import render

def index(request):
    hello_world = "Hello world woooot"
    context = {"hello_world" : hello_world}
    return render(request, "pstring/index.html", context)
def resolve_landing(request, short):
    response = "This would result in index value: "
    iv = resolve(short)
    result = response + str(iv)
    context = {"iv" : iv, "result" : result}
    return render(request, "pstring/resolve_landing.html", context)
# TO DO: function that makes database call
