from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .forms import SignUpForm, UserForm, AccountForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import Profile

# Create your views here.
class Index(TemplateView):
    template_name = 'common/index.html'

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'
    login_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['any_list'] = self.request.user
        return context


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'common/register.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/profile.html'

class ProfileUpdate(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    account_form = AccountForm
    template_name = 'common/profile-update.html'

    def post(self, request):
        data = request.POST or None
        files = request.FILES or None

        user_form = UserForm(data, instance=request.user)
        account_form = AccountForm(data, files, instance=request.user.profile)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.info(request, 'Your account is updated successfully')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(user_form=user_form, account_form=account_form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


