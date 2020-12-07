
from django.shortcuts import render
from .generator import generator 
# Create your views here.

def home(request):
    
    if request.method == 'GET':
        account_name = request.GET.get('pagename')
        submit_button = request.GET.get('submit')
        if account_name is not None:
            print(submit_button)
            account_info, post_info = generator(account_name)
            context = {
                'postData' : post_info,
                'accountData' : account_info,
                'submitButton':submit_button,
            }
            return render(request,'top_post/base.html', context) 
        else:
            return render(request,'top_post/base.html' )
    else:
        return render(request,'top_post/base.html') 