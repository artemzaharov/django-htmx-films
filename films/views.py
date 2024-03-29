from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from films.models import Film, UserFilms
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from films.forms import RegisterForm, RatingForm

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from films.utils import get_max_order, reorder
from django.shortcuts import get_object_or_404



# Create your views here.
class IndexView(FormView):
    template_name = 'index.html'
    form_class = RatingForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        print(form.cleaned_data['rating'])
        return super().form_valid(form)
    
    
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form): 
        form.save()  # save the user
        return super().form_valid(form) # call the parent method
    
def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div id="username-error" class="error">Username already exists</div>')
    else:
        return HttpResponse('<div id="username-error" class="succes">Username available</div>')
    
class FilmList(LoginRequiredMixin, ListView):
    paginate_by = 8
    model = UserFilms
    template_name = 'films.html'
    context_object_name = 'films' # name of the object in the template
    
    def get_template_names(self):
        # install django-htmx for this to work
        if self.request.htmx:
            return 'partials/film-list-elements.html'
        return 'films.html'

    def get_queryset(self):
        return UserFilms.objects.filter(user=self.request.user)

@login_required 
def add_film(request):
    name = request.POST.get('filmname')
    if name == '':
        messages.error(request, 'Film name cannot be empty')
        films = UserFilms.objects.filter(user=request.user)
        return render(request, 'partials/film-list.html', {'films': films})    
    else:
        # get_or_create returns a tuple (object, created)
        film = Film.objects.get_or_create(name=name)[0]    # add the film to the user list

        if not UserFilms.objects.filter(user=request.user, film=film).exists():
            UserFilms.objects.create(film=film, 
            user=request.user, 
            order=get_max_order(request.user)
            )
        # create a UserFilms object to manage the relationship between user and film
        # return template with all films
        films = UserFilms.objects.filter(user=request.user)
        messages.success(request, f'Film {name} added')
        return render(request, 'partials/film-list.html', {'films': films})

@login_required
# without require_http_methods, the view will be called for all http methods, but we only want to call it for DELETE
@require_http_methods(['DELETE'])
def delete_film(request, pk):
    UserFilms.objects.get(pk=pk).delete()
    reorder(request.user)
    # return template with all films
    films = UserFilms.objects.filter(user=request.user)
    return render(request, 'partials/film-list.html', {'films': films})

@login_required
def search_film(request):
    search_text = request.POST.get('search')
    userfilms = UserFilms.objects.filter(user=request.user)
    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms.values_list('film__name', flat=True)
    )
    context = {'results': results}
    return render(request, 'partials/search-results.html', context)

def clear(request):
    return HttpResponse('')

def sort(request):
    fims_pks_order = request.POST.getlist('film_order')
    films = []
    for idx, film_pk in enumerate(fims_pks_order, start=1):
        userfilm = UserFilms.objects.get(pk=film_pk)
        userfilm.order = idx
        userfilm.save()
        films.append(userfilm)
    return render(request, 'partials/film-list.html', {'films': films})

@ login_required
def detail(request, pk):
    userfilm = get_object_or_404(UserFilms, pk=pk)
    context = {'userfilm': userfilm}
    return render(request, 'partials/film-detail.html', context)

@ login_required
def films_partial(request):
    films = UserFilms.objects.filter(user=request.user)
    return render(request, 'partials/film-list.html', {'films': films})

@ login_required
def upload_photo(request, pk):
    userfilm = get_object_or_404(UserFilms, pk=pk)
    photo = request.FILES.get('photo')
    userfilm.film.photo.save(photo.name, photo)
    context = {'userfilm': userfilm}
    return render(request, 'partials/film-detail.html', context)


# def rate_view(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             rating = form.cleaned_data['rating']
#             print(rating)
#             # Do something with the rating
#             # ...
#             return render(request, 'registration/login.html')
#     else:
#         form = RatingForm()
#     return render(request, 'index.html', {'form': form})
 