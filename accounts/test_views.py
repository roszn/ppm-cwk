from django.shortcuts import render

def login_test(request):
    return render(request, 'login_test.html')
