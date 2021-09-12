from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms, get_user_model, login
from django.views.generic.edit import CreateView
from django.forms import ModelForm, RadioSelect
from django.shortcuts import redirect

from .models import Expense, Clan


class FormSectionMixin():
    def as_section(self):
        "Return this form rendered as HTML <section>s."
        return self._html_output(normal_row='<section%(html_class_attr)s data-field-name="%(field_name)s">%(label)s %(field)s%(help_text)s</section>',
                                    error_row='<aside class="error">%s</aside>',
                                    row_ender='</section>',
                                    help_text_html='<aside class="help">%s</aside>',
                                    errors_on_separate_row=False)


class AuthenticationForm(forms.AuthenticationForm, FormSectionMixin):
    pass


class SignupForm(forms.UserCreationForm, FormSectionMixin):
    class Meta:
        model = get_user_model()
        fields = ('email', )


class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


@login_required
def expenses_list(request):
    clan = request.user.clan
    if not clan:
        return redirect('clan')

    context = {
        'expenses': Expense.objects.filter(who__clan=clan).order_by('-created_at')
    }
    return render(request, "expenses_list.html", context)


class ExpenseAddForm(ModelForm, FormSectionMixin):
    class Meta:
        model = Expense
        fields = ('what', 'category', 'who', 'how_much')
        widgets = {
            'who': RadioSelect(),
            'category': RadioSelect(),
        }


class ExpenseAddView(CreateView):
    template_name = 'expenses_add.html'
    form_class = ExpenseAddForm
    success_url = 'expenses_list'

    def get_initial(self):
        initial = super().get_initial()
        initial['who'] = self.request.user
        return initial

@login_required
def clan(request):
    message = ""
    if request.method == "POST":
        code = request.POST.get('code')
        name = request.POST.get('name')
        if code:
            try:
                clan = Clan.objects.get(code=request.POST['code'])
            except Clan.DoesNotExist:
                message = "Clan does not exist"
            else:
                request.user.clan = clan
                request.user.save()
                return redirect('expenses_list')
        elif name:
            clan = Clan.objects.create(name=name)
            request.user.clan = clan
            request.user.save()
            return redirect('expenses_list')
        else:
            message = "Please add a name to your clan"
    return render(request, "clan.html", {'message': message})
