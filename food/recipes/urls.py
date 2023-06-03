from django.urls import path
from .views import *

urlpatterns = [
    path('', RecipesHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('ingredients/', IngredientsList.as_view(), name='ingredients_list'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('authors/', authors, name='authors'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('<slug:cat_slug>/', RecipesCategory.as_view(), name='category'),
    path('ingredients/<slug:ingredients_slug>/', ShowIngredients.as_view(), name='ingredients'),
]
