from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.
class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name()


class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    # upload_to: sub-carpeta donde se almacenaran las imagenes, ejm: uploads/posts/primera-imagen.jpg
    # nota: se le agrega la propiedad de "null", para evitar errores en la migracion, ya que hay datos existentes anteriormente
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True)
    # Unique: para que Django de aviso si encuentra un slug ya en uso.
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    # Si se elimina un author, el Post se establece en NULL y eso evita
    # que se elimine nuestro Post en CASCADE;
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    tag = models.ManyToManyField(Tag)


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
