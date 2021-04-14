from django.contrib import admin
from main.models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)




####################################################
class NewsAdmin(admin.ModelAdmin):
    pass

admin.site.register(News, NewsAdmin)
