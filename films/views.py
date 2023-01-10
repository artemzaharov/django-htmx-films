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

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages



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

@login_required 
def add_film(request):
    name = request.POST.get('filmname')
    if name == '':
        messages.error(request, 'Film name cannot be empty')
        return render(request, 'partials/film-list.html', {'films': request.user.films.all})    
    else:
        # get_or_create returns a tuple (object, created)
        film = Film.objects.get_or_create(name=name)[0]    # add the film to the user list
        request.user.films.add(film)
        # return template with all films
        films = request.user.films.all()
        messages.success(request, f'Film {name} added')
        return render(request, 'partials/film-list.html', {'films': films})

@login_required
# without require_http_methods, the view will be called for all http methods, but we only want to call it for DELETE
@require_http_methods(['DELETE'])
def delete_film(request, pk):
    request.user.films.remove(pk)
    # return template with all films
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})

@login_required
def search_film(request):
    search_text = request.POST.get('search')
    userfilms = request.user.films.all()
    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms.values_list('name', flat=True)
    )
    context = {'results': results}
    return render(request, 'partials/search-results.html', context)

def clear(request):
    return HttpResponse('')