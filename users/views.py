from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm,UserLoginForm,PasswordReset
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.shortcuts import redirect
class RegistrationView(FormView):
    form_class = UserRegisterForm   
    template_name='user/register.html'
    success_url='/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)
class LoginView(FormView):
    form_class = UserLoginForm
    template_name='user/login.html'
    success_url='/'

class PasswordResetView(FormView):
    form_class = PasswordReset
    template_name = "user/password_reset.html"
    success_url='/'

def ProfileView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        User = request.user
      #  profile = UserProfile.objects.get(user = User)
        parameters = {
            'user':User,
     #       'profile':profile,
        }
        return render(request, 'user/profile.html', parameters)
