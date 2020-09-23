# Django
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile

from django.views.generic import DetailView

# Forms
from users.forms import ProfileForm, SignupForm

# Create your views here.
class UserDetailView(LoginRequiredMixin, DetailView):
    """ User detail view. """
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context


def login_view(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts:feed')
        else:
            return render(request, 'users/login.html', {'error': 'Username y contraseña invalido'})

    return render(request, 'users/login.html')


def signup_view(request):
    """Signup view"""
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form.SignupForm()

    return render(
        request=request, 
        template_name='users/signup.html', 
        context={'form': form}
    )  
          

@login_required
def update_profile(request):
    """ Update profile view """
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)  
            data = form.cleaned_data

            profile.username = data['username']
            profile.first_name = data['first_name']
            profile.last_name = data['last_name']
            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.email = data['email']
            profile.save()

            url = reverse('users:detail', kwargs={'username': request.user.username})
            return redirect(url)   
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
    return redirect('users:login')