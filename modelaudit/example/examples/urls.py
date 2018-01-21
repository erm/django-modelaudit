from django.urls import path
from django.conf.urls import include

from examples.views import (
    example_create_view,
    example_update_view,
    example_detail_view,
)


example_patterns = ([
    path(
        'create/',
        example_create_view,
        name='create'
    ),
    path(
        'update/<int:pk>',
        example_update_view,
        name='update'
    ),
    path(
        'detail/<int:pk>',
        example_detail_view,
        name='detail'
    ),
], 'examples')


urlpatterns = [
    path('', include(example_patterns)),
]
