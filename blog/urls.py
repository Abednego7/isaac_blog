from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    # /posts/my-first-post: los 'segmentos dinamicos' con este aspecto (x-1-), contiene caracteres, numeros, guiones y se denominan "slug",
    # un identificador amigable para los motores de busqueda.
    # Al igual que con los constructores str, int, etc, Django tiene uno especial para los slug:
    # Nota: este slug (dato dinamico) pasara a ser parte de la creacion de la funcion y sera parte de los parametros de esta,
    # ejm: def show_slug(request, slug)
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="post-detail-page"),
]
