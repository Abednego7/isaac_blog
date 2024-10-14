from django.urls import path
from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("posts", views.posts, name="posts-page"),
    # /posts/my-first-post: los 'segmentos dinamicos' con este aspecto (x-1-), contiene caracteres, numeros, guiones y se denominan "slug",
    # un identificador amigable para los motores de busqueda.
    # Al igual que con los constructores str, int, etc, Django tiene uno especial para los slug:
    path("posts/<slug:slug>", views.post_detail, name="post-detail-page"),
]
