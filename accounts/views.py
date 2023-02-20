from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from contacts.models import Contact
# Create your views here.


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        isValid = True
        #password match
        if password != password2:
            isValid = False
            messages.error(request,'passwords doesnt match')
        #username and email check
        if User.objects.filter(username=username).exists():
            isValid = False
            messages.error(request,'Username already exisits')
        
        if User.objects.filter(email=email).exists():
            isValid = False
            messages.error(request,'Email already exisits')    

        if isValid == False:
            context = {
                'values':request.POST
            }
            return(render(request,'accounts/register.html',context))
        else:
            user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
            user.save()
            messages.success(request,'Your account created, You can login now')
            return redirect('login')

        
    else:
        return render(request,'accounts/register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged In')
            return redirect('dashboard')
        
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'Successfully logged out !')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts' : user_contacts
    }
    return render(request,'accounts/dashboard.html',context)


