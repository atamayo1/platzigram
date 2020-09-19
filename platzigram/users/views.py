# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Models
from django.contrib.auth.models import User
from users.models import Profile

# Forms
from users.forms import ProfileForm

# Create your views here.
def login_view(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        else:
            return render(request, 'users/login.html', {'error': 'Username y contraseña invalido'})

    return render(request, 'users/login.html')


def signup_view(request):
    """Signup view"""
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if password != confirm_password:
           return render(request, 'users/signup.html', {'error': 'La contraseña de confirmación es incorrecta'})
        else:
            try:
                user = User.objects.create_user(username=username, password=password)
            except:
                return render(request, 'users/signup.html', {'error': 'Username ya esta creado'})

            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            profile = Profile(user=user) 
            profile.save()
            return redirect('login')

    return render(request, 'users/signup.html')        


def update_profile(request):
    """ Update profile view """
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)  
            data = form.cleaned_data

            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.save()

            return redirect('update_profile')   
    else:
        form = ProfileForm()    

    """Update view"""
    return render(
        request=request, 
        template_name='users/update_profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': form,
        }
    )  

@login_required
def logout_view(request):
    """ Logout a user. """
    logout(request)
    return redirect('login')