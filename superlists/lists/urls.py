from django.urls import path, re_path

import lists.views

urlpatterns = [
    path('', lists.views.home_page, name='home'),
    re_path('^(\d)/$', lists.views.list_view, name='list_view'),
    re_path('^(\d)/add_item$', lists.views.add_item, name='add_item'),
    path('new', lists.views.new_list, name='new_list'),
]
