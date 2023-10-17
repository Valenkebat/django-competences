from django.db import models
from .competition import Competition
import random

from django.db import models

from matches.models import Match, MapPoolChoice, MapChoice
from matches.settings import TEAMFORMAT_CHOICES, MAPFORMAT_CHOICES
from profiles.models import User
from teams.models import Team

SIZE_CHOICES = (
    (4, 4),
    (8, 8),
    (16, 16),
    (32, 32),
    (64, 64),
    (128, 128),
)

class SingleEliminationCompetition(models.Model):
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE, parent_link=True)

    # all the teams that are in the event. eligibility happens inside the view, 
    # when they try to register @ben told me
    #  how to do this mtm field, i forgot
    teams = models.ManyToManyField(Team, blank=True)

    current_round = models.SmallIntegerField(default=1, blank=True)

    # specify the winning team when they are declared
    winner = models.ForeignKey(Team, related_name='winningteam', on_delete=models.SET_NULL, blank=True, null=True)

    # specify second place, just for storage and future reference
    second = models.ForeignKey(Team, related_name='secondplaceteam', on_delete=models.SET_NULL, blank=True, null=True)

    third = models.ForeignKey(Team, related_name='thirdplaceteam', on_delete=models.SET_NULL, blank=True, null=True)

    # specify how many teams the event will be capped at, and the size of the bracket
    size = models.PositiveSmallIntegerField(default=32, choices=SIZE_CHOICES)

    xp_seed = models.BooleanField(default=False)

    bracket_generated = models.BooleanField(default=False)

    map_pool = models.ForeignKey(MapPoolChoice, related_name='map_pool', on_delete=models.SET_NULL, null=True)

    # the prizes that they will win, defined in admin panel. 3rd place isnt really needed..... just first and second...
    prize1 = models.CharField(default='no prize specified', max_length=50)
    prize2 = models.CharField(default='no prize specified', max_length=50)
    prize3 = models.CharField(default='no prize specified', max_length=50)

    image = models.ImageField(upload_to='tournament_images', blank=True)

    # if set to true, admins will have manually input the result of each match, users will not be able to report wins
    # when matches are created it will set the match field to whatever this field is set to.
    disable_userreport = models.BooleanField(default=True)

    # need to figure out how we will work rules rules = models.ForeignKey(Ruleset, related_name='tournamentrules',
    # on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.name  # + self.platform + self.game

    def generate_maps(self, roundpk):
        pool = self.map_pool
        poolsize = pool.maps.count()
        try:
            round = SingleEliminationRound.objects.get(id=roundpk)
        except:
            return False
        if round:
            matches = round.matches
            for match in matches:
                mike = random.random(1, poolsize)
                temp_map = MapChoice.objects.get(map_num=mike)
                match.map = temp_map

    def set_inactive(self, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationCompetition.objects.get(id=pk)
        tournament.active = False
        tournament.save()

    def generate_bracket(self):
       teams = len(self.teams.all())
       myteams = self.teams.all()
       self.current_round = 1
       self.save()
       round1 = SingleEliminationRound(tournament=self, roundnum=1)
       round1.save()
       if teams % 2 == 0:
           # no byes required - get 2 teams and make a match
           while len(myteams) != 0:
               temp1 = myteams.all().order_by("?").first()
               myteams.remove(temp1)
               myteams.save()
               temp2 = myteams.all().order_by("?").first()
               tempmatch = Match(awayteam=temp1, hometeam=temp2, maps=self.map_pool, game=self.game, platform=self.platform)
               tempmatch.save()
               myteams.remove(temp2)
               myteams.save()
               round1.matches.add(tempmatch)
               round1.save()

       else:
           # take the first team and give them a bye
           # TODO: verify this randomly grabs a random team
           bteam = self.teams.all.order_by("?").first()
           bmatch = Match(hometeam=None, bye_1=True, awayteam=bteam, winner=bteam, completed=True,
                          type='singletournament', maps=self.map_pool, game=self.game, platform=self.platform)
           bmatch.save()
           round1.matches.add(bmatch)
           myteams.remove(bteam)
           if len(myteams) % 2 != 0:
               print("ITS BROKEN YOU SUCK")
               return
           while len(myteams) != 0:
               temp1 = myteams.all().order_by("?").first()
               myteams.remove(temp1)
               myteams.save()
               temp2 = myteams.all().order_by("?").first()
               tempmatch = Match(awayteam=temp1, hometeam=temp2, maps=self.map_pool, game=self.game, platform=self.platform)
               tempmatch.save()
               myteams.remove(temp2)
               myteams.save()
               round1.matches.add(tempmatch)
               round1.save()

       round1.save()

    def get_round1_byes(self, **kwargs):
        # only used for round 1 purposes
        pk = self.kwargs['pk']
        tournament = SingleEliminationCompetition.objects.get(id=pk)
        return tournament.size - tournament.teams.count

    def get_num_teams(self):
        return self.teams.count


class SingleEliminationRound(models.Model):
    # ManyToManyField to keep track of the teams that are still active and have matches to play in the round
    # teams = models.ManyToManyField(Team)

    # what round number is this? round 1 is the first round of the tournament
    roundnum = models.PositiveSmallIntegerField(default=1)

    # how many matches will be played in this round? Set the default to the minimum
    matchesnum = models.PositiveSmallIntegerField(default=2)

    tournament = models.ForeignKey(SingleEliminationCompetition, related_name='withtournamentround',
                                   on_delete=models.CASCADE)

    # ManyToMany Field to keep track of the matches that were assigned and created for this given round...
    matches = models.ManyToManyField(Match)

    info = models.TextField(default='No info specified')


class SingleEliminationTeam(models.Model):
    team = models.ForeignKey(Team, related_name='actualteam', null=True, on_delete=models.CASCADE)
    seed = models.PositiveIntegerField(default=0, null=True, blank=True)
    tournament = models.ForeignKey(SingleEliminationCompetition, related_name='intournament', null=True,
                                   on_delete=models.CASCADE)