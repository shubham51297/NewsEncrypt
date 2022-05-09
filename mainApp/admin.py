from django.contrib import admin
from .models import User,Source,Editor,NewsTip
# Register your models here.

admin.site.register(User)
admin.site.register(Source)
admin.site.register(Editor)

admin.site.register(NewsTip)