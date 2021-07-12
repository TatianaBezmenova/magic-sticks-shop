from django.views.decorators.http import require_POST
from django.views.generic import DetailView, UpdateView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import UserRegForm


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    context_object_name = 'object'


class UserUpdateView(UpdateView):
    model = User
    slug_field = 'username'
    fields = ['email', 'first_name', 'last_name']

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object():
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = 'user/user_login.html'


class UserRegistrationView(FormView):
    form_class = UserRegForm
    template_name = 'user/user_reg.html'

    def form_valid(self, form: UserRegForm):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create_user(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect('/')


@require_POST
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
