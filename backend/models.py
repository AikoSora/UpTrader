from django.db import models


class MenuItem(models.Model):
    title = models.TextField(default="Меню")
    url = models.TextField(default="/")
    parents = models.ManyToManyField("MenuItem", blank=True)

    def __str__(self):
        return self.title.title()


class Menu(models.Model):
    name = models.TextField(default="menu")
    menu_items = models.ManyToManyField(MenuItem)

    def __str__(self):
        return self.name
