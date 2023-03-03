import os

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import * # от туда берём MENU, а также DataMixin


# Create your views here.
menu = MENU


class TravelHome(DataMixin, ListView):
    model = Travel # получает все записи из таблицы
    template_name = 'travel/index.html'
    context_object_name = 'tours' # название передаваемой переменной в шаблон (вместо object_list)
    #extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        # методу get_context_data() можно передавать и статические и динамические данные
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница', departure_selected=0)
        context.update(c_def)
        #print(context)
        return context

    def get_queryset(self):
        # метод, в котором можно указать как именно выбирать записи из модели Travel
        return Travel.objects.filter(is_published=True).select_related('dep')
        #return Travel.objects.filter(is_published=True)


class TravelDeparture(DataMixin, ListView):
    model = Travel  # получает все записи из таблицы
    template_name = 'travel/departure.html'
    context_object_name = 'tours'
    allow_empty = False # если список пустой, то выдаст ошибку 404

    def get_context_data(self, *, object_list=None, **kwargs):
        # методу get_context_data() можно передавать и статические и динамические данные
        context = super().get_context_data(**kwargs)
        # title = 'Отправление ' + str(Departure.objects.get(pk=context['tours'][0].dep_id))
        title = 'Отправление ' + str(Departure.objects.get(slug=self.kwargs['departure_slug']))
        c_def = self.get_user_context(title=title, departure_selected=self.kwargs['departure_slug'])
        context.update(c_def)
        return context
        # context['menu'] = menu
        # context['title'] = 'Отправление ' + str(Departure.objects.get(pk=context['tours'][0].dep_id))
        # context['departure_selected'] = self.kwargs['departure_slug']
        # return context

    def get_queryset(self):
        # метод, в котором можно указать как именно выбирать записи из модели Travel
        return Travel.objects.filter(is_published=True, dep__slug=self.kwargs['departure_slug']).select_related('dep')


class ShowTour(DataMixin, DetailView):
    model = Travel
    template_name = 'travel/tour.html'
    slug_url_kwarg = 'tour_slug'
    # pk_url_kwarg = 'tour_id'
    context_object_name = 'tour'

    def get_context_data(self, *, object_list=None, **kwargs):
        # методу get_context_data() можно передавать и статические и динамические данные
        # context['menu'] = menu
        # context['title'] = context['tour'].title
        context = super().get_context_data(**kwargs)
        title = context['tour'].title
        c_def = self.get_user_context(title=title)
        context.update(c_def)
        return context


class AddTour(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTourForm
    template_name = 'travel/addtour.html'
    # success_url = reverse_lazy('home') # после добавления поста, если прописан get_absolute_url, то джанго автоматически перевёд на страницу созданного тура
    # а если нет, то будет ошибка, чтобы этого не было, то эта функция вернёт на Home
    login_url = reverse_lazy('admin') #если пользователь не авторизирован, то попадёт на эту страницу
    #raise_exception = True # будет выдавать ошибку 403, если не авториз пользователь

    def get_context_data(self, *, object_list=None, **kwargs):
        # методу get_context_data() можно передавать и статические и динамические данные
        context = super().get_context_data(**kwargs)
        # context['menu'] = menu
        # context['title'] = 'Добавление тура'
        c_def = self.get_user_context(title='Добавление тура')
        context.update(c_def)
        return context


class RegisterUser(DataMixin, CreateView):
    #form_class = UserCreationForm # стандартная форма от джанго
    form_class = RegisterUserForm  # собственная форма
    template_name = 'travel/register.html' # ссылка на шаблон
    success_url = reverse_lazy('login') # при успешной регистрации перенаправит по этому пути

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context.update(c_def)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    # form_class = AuthenticationForm
    form_class = LoginUserForm
    template_name = 'travel/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        context.update(c_def)
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class AboutPageView(DataMixin, TemplateView):
    template_name = "travel/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О нас")
        context.update(c_def)
        return context


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = "travel/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        context.update(c_def)
        return context

    def form_valid(self, form):
        # Этот метод вызывается, когда были опубликованы действительные данные формы.
        # Он должен возвращать HttpResponse.
        form.send_email()
        return redirect('home')





# def contact(request):
#     return HttpResponse("Обратная связь")


# def about(request):
#     # return HttpResponse(f"<h1>about</h1>")
#     context = {'menu': MENU,
#                'title': 'О нас',
#                }
#     context = super().get_context_data(**kwargs)
#     return render(request, 'travel/about.html', context=context)


# def login(request):
#     return HttpResponse("Авторизация")


# def index(request):
#     tours = Travel.objects.all()
#     context = {'tours': tours,
#                'menu': menu,
#                'title': 'Главная страница',
#                'departure_selected': 0,
#                }
#     return render(request, 'travel/index.html', context=context)
#     #return HttpResponse("<h1>Я страница HOME</h1>")


# def show_departure(request, departure_slug):
#     # tours = Travel.objects.filter(pk=departure_id)
#     # tours = Travel.objects.filter(dep__slug=departure_slug)
#     tours = get_list_or_404(Travel, dep__slug=departure_slug)
#
#     # if not len(tours):
#     #     raise Http404()
#
#     context = {'tours': tours,
#                'menu': menu,
#                'title': 'Отправление из',
#                'departure_selected': departure_slug,
#                }
#     return render(request, 'travel/departure.html', context=context)
#
# def departure(request, departure_id):
#     return render(request, departure_id, 'travel/departure.html', {'title': 'О сайте'})
#     #return HttpResponse("<h1>Я страница DEPARTURE</h1>")


# def show_tour(request, tour_slug):
#     #tour = get_object_or_404(Travel, pk=tour_id)
#     tour = get_object_or_404(Travel, slug=tour_slug)
#     context = {'tour': tour,
#                'menu': menu,
#                'title': tour.title,
#                'departure_selected': tour.dep_id,
#                }
#     return render(request, 'travel/tour.html', context=context)


# def addtour(request):
#     if request.method == 'POST':
#         form = AddTourForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             '''для не связанных форм
#             try:
#                 Travel.objects.create(**form.cleaned_data)
#
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#             '''
#             form.save()  # для связанных форм
#             return redirect('home')
#     else:
#         form = AddTourForm()
#     context = {'menu': menu,
#                'title': 'Добавление тура',
#                'form': form,
#                }
#
#     return render(request, 'travel/addtour.html', context=context)











