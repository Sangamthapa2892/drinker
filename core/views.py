from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact,Testimonial,LiquorCategory,Subscriber,Liquor
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings
import re

# Create your views here.
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        phone_pattern = r'^\+\d{1,4}\d{7,10}$'
        valid_phone = re.match(phone_pattern, phone)

        if not (name and phone and email and message):
            messages.error(request, 'All credentials are required.')
        elif not is_valid_email(email):
            messages.error(request, 'Invalid email format.')
        elif not valid_phone:
            messages.error(request, 'Phone number must be in international format (e.g., +1234567890).')
        elif Contact.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
        else:
            # Save contact first
            contact = Contact.objects.create(name=name, phone=phone, email=email, message=message)
            messages.success(request, 'Your message has been saved successfully!')
            
            try:
                # Send confirmation email
                send_mail(
                    subject='Thank you for contacting us!',
                    message=f"Hi {name},\n\nWe've received your message and will get back to you soon.\n\nYour message: {message}\n\nCheers,\nTeam",
                    from_email='sangamthapa2892@gmail.com',  # Explicitly set from email
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Confirmation email sent!')
            except Exception as e:
                # Log the error but don't show to user
                print(f"Email sending failed: {e}")
                # You can optionally show a warning message
                messages.warning(request, 'Message saved but confirmation email failed to send.')
    
    testimonials = Testimonial.objects.all()
    categories = LiquorCategory.objects.all()
    context = {
        'testimonials': testimonials,
        'categories': categories,
    }
    return render(request, 'core/index.html', context)

def about(request):
    return render(request,'core/about.html')

def store(request):
    liquors = Liquor.objects.all()
    categories = LiquorCategory.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        liquors = Liquor.objects.filter(category__name=selected_category)
    else:
        liquors = Liquor.objects.all()

    context = {
        'categories':categories,
        'liquors':liquors,
        'selected_category': selected_category,

    }
    return render(request,'core/store.html',context)

def review(request):
    testimonials = Testimonial.objects.all()
    return render(request,'core/review.html',{'testimonials':testimonials})

def contact(request):
    if request.method=='POST':
        name = request.POST.get('name').strip()
        phone = request.POST.get('phone').strip()
        email = request.POST.get('email').strip()
        message = request.POST.get('message').strip()
        
        phone_pattern = r'^\+\d{1,4}\d{7,10}$'
        valid_phone = re.match(phone_pattern, phone)

        if not (name and phone and email and message):
            messages.error(request, 'All credentials are required.')
        elif not is_valid_email(email):
            messages.error(request, 'Invalid email format.')
        elif not valid_phone:
            messages.error(request, 'Phone number must be 10 digits.')
        elif Contact.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
        else:
            Contact.objects.create(name=name, phone=phone, email=email, message=message)
            messages.success(request, 'Your message has been saved successfully !!!')
            send_mail(
                subject='Thank you for contacting us!',
                message=f"Hi {name},\n\nWe've received your message and will get back to you soon.\n\nCheers,\nTeam",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=False,
            )
        
    return render(request,'core/contact.html')



def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email or not is_valid_email(email):
            messages.error(request, "Please enter a valid email address.")
        else:
            if not Subscriber.objects.filter(email=email).exists():
                Subscriber.objects.create(email=email)
                request.session['subscribed'] = True
                messages.success(request, "Thanks for subscribing!")
            else:
                print('ok')
                messages.info(request, "You're already subscribed.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def broadcast_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipients = Subscriber.objects.filter(is_active=True).values_list('email', flat=True)
        send_mail(subject, message, 'sangamthapa2892@gmail.com', list(recipients))
        messages.success(request, f"Email sent to {len(recipients)} subscribers.")
    return render(request, 'broadcast.html')

'''
====================== Accounts section =====================

'''

def login_view(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or '/'

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': next_url})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password'})

    return JsonResponse({'success': False, 'error': 'Invalid request type'})



def register_view(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Passwords do not match!'})

        if User.objects.filter(username=uname).exists():
            return JsonResponse({'success': False, 'error': 'Username already taken!'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered!'})

        user = User.objects.create_user(
            username=uname,
            email=email,
            password=password1,
            first_name=fname,
            last_name=lname
        )
        user.save()
        send_mail(
                subject='Thank you for contacting us!',
                message=f"Hi {uname},\n\nThankyou for connecting with us !!!\n\nCheers,\nTeam",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=False,
            )

        return JsonResponse({'success': True})

def logout_view(request):
    logout(request)
    return redirect('/?logged_out=true')

