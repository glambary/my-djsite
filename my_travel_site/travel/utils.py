from django.db.models import Count

from .models import *


MENU = [{'title': "О нас", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        # {'title': "Войти", 'url_name': 'login'},
        ]
menu_hidden = [{'title': "Добавить тур", 'url_name': 'addtour'},
               {'title': "Админка", 'url_name': 'admin'},
               ]
menu_hidden = []


class DataMixin:
    paginate_by = 3  # Пагинация

    def get_user_context(self, **kwargs):
        context = kwargs
        # deps = Departure.objects.all()
        deps = Departure.objects.annotate(Count('travel')) # вариант черех проверку в шаблоне

        if self.request.user.username != 'root':
            menu_hidden.clear()
        context['menu'] = MENU
        context['menu_hidden'] = menu_hidden

        context['departuress'] = deps
        # if 'departure_selected' not in context:
        #     context['departure_selected'] = 0
        return context
