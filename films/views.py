from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from films.models import Film
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from films.forms import RegisterForm



# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)
    
def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div id="username-error" class="error">Username already exists</div>')
    else:
        return HttpResponse('<div id="username-error" class="succes">Username available</div>')
    
class FilmList(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Film
    template_name = 'films.html'
    context_object_name = 'films'
    
    def get_queryset(self):
        user = self.request.user
        return user.films.all()
    
def add_film(request):
    name = request.POST.get('filmname')
    film = Film.objects.create(name=name)
    # add the film to the user list
    request.user.films.add(film)
    # return template with all films
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})



