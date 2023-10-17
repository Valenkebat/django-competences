from django.contrib import admin
from .models import Competition, league, singleElimination

admin.site.register(Competition)
admin.site.register(league.LeagueCompetition)
admin.site.register(league.LeagueDivision)
admin.site.register(league.LeagueSettings)
admin.site.register(league.LeagueTeam)
admin.site.register(singleElimination.SingleEliminationCompetition)
admin.site.register(singleElimination.SingleEliminationRound)
admin.site.register(singleElimination.SingleEliminationTeam)

