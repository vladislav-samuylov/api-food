from django.db.models import Count

from .models import *

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "База", 'url_name': 'home'},
        {'title': "Ингредиенты", 'url_name': 'ingredients_list'},
        {'title': "Авторы", 'url_name': 'home'}]

class DataMixin:
    paginate_by = 5
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('recipes'))
        context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
