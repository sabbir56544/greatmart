from django.shortcuts import redirect, render
from .forms import UserLoginForm, UserCreateForm
from .models import Profile
from django.contrib.auth.models import Group
from django.http.response import HttpResponse

#send mail
from django.core.mail import send_mail

#authentication for login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.contrib.auth.models import auth, User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# verification_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.views.generic import View




def sign_up_view(request):
    form = UserCreateForm()

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name="customer")
            user.groups.add(group)
            user_profile = Profile.objects.get_or_create(user=user)

            #activation

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('accounts/verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))
            
            mydict = {'username': username}
            html_template = 'accounts/register_email.html'
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Welcome to Service-Verse'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            return redirect('waiting')
        else:
            messages.warning(request, "This Username or email already exist plz try again")
        
    context = {
        'form': form,
        'error': "This Username is already taken",
    }
    return render(request, 'accounts/signup.html', context)



def log_in(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Invalid Email or Password!!")
                
            context = {
                'form': form,
            }
            return render(request, 'accounts/login.html', context)
        

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)



@login_required
def log_out(request):
    logout(request)
    return redirect('home')


def activation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None    

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congrats")
    else:
        messages.warning(request, "Ouydygh")
        return redirect('register')       


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')


def waiting(request):
    return render(request, 'accounts/waiting.html')
