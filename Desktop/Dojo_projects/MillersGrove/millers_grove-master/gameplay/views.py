from django.shortcuts import render, redirect, HttpResponse

def gameplay(request):
    return HttpResponse("You have reached the GAMEPLAY MAIN route")