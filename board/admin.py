from django.contrib import admin

from board.models import Article


# Register your models here.

@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ["a_title", "a_tree_image", "a_man_image", "a_woman_image", "a_house_image"]
