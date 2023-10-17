from django.contrib import admin

# Register your models here.

from .models import Match, MapChoice, MapPoolChoice, MatchCheckIn

admin.site.register(Match)
admin.site.register(MapChoice)
admin.site.register(MapPoolChoice)
admin.site.register(MatchCheckIn)