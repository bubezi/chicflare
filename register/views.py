from django.shortcuts import render, redirect
from .forms import UserSignUpForm, ChangeUserDetailsForm
from django.contrib.auth import authenticate, login
from django.contrib.sites.models import Site
# from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import SignupLink
from django.http import HttpResponseBadRequest
# from django.http import HttpResponse
from .myFunctions import check_errors


def generate_link(request):
    link = get_random_string(length=35)
    expiry_time = timezone.now() + timezone.timedelta(minutes=10)
    SignupLink.objects.create(link=link, expired_time=expiry_time)
    site = Site.objects.get(id=1)
    # signup_url = 'http://' + site.domain + '/register/' + link
    ##Comment out during production
    signup_url = 'https://' + site.domain + '/register/' + link
    # return HttpResponse(signup_url)
    context = {'signup_url': signup_url}
    if request.user.is_superuser:
        return render(request, 'register/generate_link_page.html', context)
    else:
        return HttpResponseBadRequest('Invalid Request')


# Create your views here.
def register(request, link):
    try:
        signup_link = SignupLink.objects.get(link=link)
        if not signup_link.is_valid():
            raise SignupLink.DoesNotExist
    except SignupLink.DoesNotExist:
        return HttpResponseBadRequest('Invalid link')
    if request.method == "POST":
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            signup_link.used = True
            signup_link.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('/')
        else:
            errors = check_errors(form)
            form = UserSignUpForm()
            context = {"form": form, "errors": errors}

    else:
        form = UserSignUpForm()
        context = {"form": form}

    return render(request, "register/register.html", context)


def bye_page(request):
    context = {}
    return render(request, "bye/bye.html", context)


def profile_page(request):
    customer = request.user.customer
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangeUserDetailsForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.save()
                return render(request, "profile/profile.html", context={'customer': customer, "form": form})
            else:
                errors = check_errors(form)
                form = ChangeUserDetailsForm(request.POST, request.FILES, instance=customer)
                context = {'customer': customer, "form": form, "errors": errors}

        else:
            form = ChangeUserDetailsForm()
            context = {'customer': customer, "form": form}
        return render(request, "profile/profile.html", context)
    else:
        return redirect('login')
