from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ContactForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/contact')
            
        
    else:
        form = ContactForm()

    return render(request, 'contact.html', {form: form})

@login_required
def diabetes(request):
    if request.method == 'POST':
        try:
            sugar_level_before = int(request.POST.get('sugar_level_before'))
            sugar_level_after = int(request.POST.get('sugar_level_after'))
        except (ValueError, TypeError):
            messages.error(request, "Please enter valid numbers for blood sugar levels.")
            return render(request, 'diabetes.html')

      
        if 70 <= sugar_level_before <= 99 and sugar_level_after < 140:
            messages.info(request, "Diabetic Level: Normal!")
        
      
        elif 100 <= sugar_level_before <= 125 and 140 <= sugar_level_after <= 199:
            messages.info(request, "Diabetic Level: Prediabetes!")
        
       
        elif sugar_level_before >= 126 and sugar_level_after >= 200:
            messages.info(request, "Diabetic Level: Diabetes!")
        
       
        else:
            messages.warning(request, "Blood sugar levels do not match typical categories. Please consult a healthcare provider.")

    return render(request, 'diabetes.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
         
       
        if not User.objects.filter(username=username).exists():
    
            messages.error(request, 'Invalid Username')
            return redirect('/login')
         
      
        user = authenticate(username=username, password=password)
         
        if user is None:
            
            messages.error(request, "Invalid Password")
            return redirect('/login')
        else:
           
            login(request, user)
            return redirect('/')
     
    
    return render(request, 'login.html')
 
 
def register(request):
    try:
        if request.method == 'POST':
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            
            user = User.objects.filter(username=username)
            
            if user.exists():
            
                messages.info(request, "Username already taken!")
                return redirect('/register')
            
            
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username
            )
            
    
            user.set_password(password)
            user.save()
            
            
            messages.info(request, "Account created Successfully!")
            return redirect('/login')

    except ValueError:
        return render(request, 'register.html')

        
    return render(request, 'register.html')