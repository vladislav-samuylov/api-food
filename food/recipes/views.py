from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .models import *
from .forms import *
from .utils import *


class RecipesHome(DataMixin, ListView):
    model = Recipes
    template_name = 'recipes/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Recipes.objects.filter(is_published=True)


# def index(request):
#     posts = Recipes.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница'
#     }
#     return render(request, 'recipes/index.html', context=context)

def about(request):
    cats = Category.objects.annotate(Count('recipes'))
    return render(request, 'recipes/about.html', {'menu': menu, 'title': 'О сайте', 'cats': cats})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'recipes/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление рецепта")
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'recipes/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление рецепта'})

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'recipes/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Recipes
    template_name = 'recipes/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Recipes, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'recipes/post.html', context=context)

class RecipesCategory(DataMixin, ListView):
    model = Recipes
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Recipes.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_slug):
#     posts = Recipes.objects.filter(cat__slug=cat_slug)
#     c = Category.objects.get(slug=cat_slug)
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Категория - ' + str (c.name),
#         'cat_selected': cat_slug,
#     }
#
#     return render(request, 'recipes/index.html', context=context)

class ShowIngredients(DataMixin, DetailView):
    model = Ingredient
    template_name = 'recipes/ingredient.html'
    slug_url_kwarg = 'ingredients_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_ingredients(request, ingredients_slug):
#     post = get_object_or_404(Ingredient, slug=ingredients_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.name,
#         'cat_selected': ingredients_slug,
#     }
#
#     return render(request, 'recipes/ingredient.html', context=context)

class IngredientsList(DataMixin, ListView):
    model = Ingredient
    template_name = 'recipes/ingredients_list.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Ингредиенты")
        return dict(list(context.items()) + list(c_def.items()))


# def ingredients_list(request):
#     posts = Ingredient.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Ингредиенты'
#     }
#     return render(request, 'recipes/ingredients_list.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'recipes/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'recipes/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def authors(request):
    posts = Recipes.objects.all()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'recipes/authors.html', context=context)