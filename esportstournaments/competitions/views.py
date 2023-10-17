import datetime
import pytz
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View
from competitions.models.singleElimination import SingleEliminationRound, SingleEliminationTeam

from profiles.models import UserProfile
from teams.models import Team
from .forms import CompetitionJoinGet, CompetitionJoinPost, \
    CompetitionSort, CompetitionLeaveForm, CompetitionCreateForm
from .models import Competition, SingleEliminationCompetition
from .strategies.factory import CompetitionFactory
import asyncio


class CreateCompetition(View):
    pass

class List(View):

    def get(self, request):
        competition_list = Competition.objects.all().filter(active=True)

        return render(request, 'competition/competition_list.html',
                      {'competition_list': competition_list})

    def post(self, request):
        form = CompetitionCreateForm(self.request.POST or None)
        
        #Arreglar
        if(form.is_valid()):
            competition =  CompetitionCreateForm.create_competition()

        tournament_list =  Competition.objects.all().filter(active=True)
        return  render(request, 'competition/competition_list.html',
                      {'competition_list': tournament_list, 'form': form})


class SingleTournamentJoin(View):

    def get(self, request, pk):
        # teaminvites = TeamInvite.objects.filter(user_id=request.user.id, hasPerms=True)
        profile = UserProfile.objects.get(user=request.user)
        teams = profile.founder_teams.all() | profile.captain_teams.all()
        competition = get_object_or_404(Competition, id=pk)
        if teams.count() != 0:
            form = CompetitionJoinGet(request)
            return render(request, 'competition/competition_join.html',
                          {'form': form, 'competition': competition})
        else:
            messages.error(request, message="You aren't a captain or founder of any team!")
            return redirect('competition:list')

    def post(self, request, pk):
        form = CompetitionJoinPost(request.POST)
        profile = UserProfile.objects.get(user=request.user)
        team = Team.objects.get(id=int(form.data['teams']))
        if team in profile.captain_teams.all() or team in profile.founder_teams.all():
            # good to go
            pass
        else:
            messages.error(request, message="You aren't a captain or founder of this team")
            return redirect('competition:list')

        competition = Competition.objects.get(id=self.kwargs['pk'])
        if competition.teamformat == 0:
            players = 1
        elif competition.teamformat == 1:
            players = 2
        elif competition.teamformat == 2:
            players = 3
        elif competition.teamformat == 3:
            players = 4
        else:
            messages.error(request, "Tournament minimum player error-unable to join tournament")
            return redirect('singletournaments:detail', pk=competition.pk)
        # team = Team.objects.get(id=int(form.data['teams']))
        # users = TeamInvite.objects.filter(team=form.data['teams'], accepted=True)
        registered_teams = competition.teams.all()
        teameligible = False
        utc = pytz.UTC
        now = utc.localize(datetime.datetime.now())

        if competition.open_register >= now:
            messages.error(request, 'Registration for this tournament is not open yet')
            return redirect('competition:list')

        if competition.close_register <= now:
            messages.error(request, 'Registration for this tournament is closed already')
            return redirect('competition:list')

        # this allows for a manual override of registration - not recommended
        # if you'd like to allow teams after the fact we recommend force adding teams via staff panel
        """if not tournament.allow_register:
            messages.error(request, 'Registration for this tournament is not open currently')
            return redirect('competition:list')

        """

        if competition.bracket_generated:
            messages.error(request, "The bracket has already been generated for this tournament, new teams aren't "
                                    "permitted")
            return redirect('competition:list')

        if registered_teams.count() >= competition.size:
            messages.error(request, "This tournament is full")
            return redirect('competition:list')
        for player in team.players:
            user = UserProfile.objects.get(user=player)
            # logic like below allows for verification of xbl/psn/steam accounts linked
            """if not user.xbl_verified and tournament.platform == 1:
                teameligible = False
                messages.error(request, "One or more users does not have Xbox Live set")
                return redirect('teams:list')
            elif not user.psn_verified and tournament.platform == 0:
                teameligible = False
                messages.error(request, "One or more users does not have PSN set")
                return redirect('teams:list')"""
            if int(user.credits) < int(competition.req_credits):
                teameligible = False
                messages.error(request, "One or more players does not have enough credits")
                return redirect('teams:list')
            else:
                teameligible = True
            if not teameligible:
                messages.error(request, "Not all members of your team are eligible to join")
        if len(team.players) + len(team.captain) + len(team.founder) <= players:
            teameligible = False
            messages.error(request, "Your team does not have enough people to play in this tournament")
        if not teameligible:
            messages.error(request, "There was an issue with team eligibility for this tournament")
            return redirect('teams:list')
        if team in competition.teams:
            messages.error(request, message="This team is already in this tournament")
            return redirect('singletournaments:list')
        # loop through every user on the team trying to join - see if they're a player/founder/captain
        # on any other team thats already registered
        for user in team.players.all():
            for otherteam in competition.teams.all():
                for player in otherteam.players.all():
                    if user == player:
                        messages.error(request, "There is overlap between users in teams in the tournament")
                        return redirect('singletournaments:list')
                for captain in otherteam.captain.all():
                    if user == captain:
                        messages.error(request, "There is overlap between users in teams in the tournament")
                        return redirect('singletournaments:list')
                if user == otherteam.captain.all():
                    messages.error(request, "There is overlap between users in teams in the tournament")
                    return redirect('singletournaments:list')

        competition.teams.add(team)
        competition.save()
        tournament_team = SingleEliminationTeam(team_id=team.id, tournament_id=competition.id)
        tournament_team.save()
        messages.success(request, message="Joined tournament")
        return redirect('singletournaments:list')


class SingleTournamentLeave(View):
    def get(self, request, pk):
        form = CompetitionLeaveForm()
        return render(request, 'singletournaments/singletournament_leave.html', {'form': form})

    def post(self, request, pk):
        form = CompetitionLeaveForm(request.POST)
        competition = Competition.objects.filter(id=pk)
        user_teams = Team.objects.filter(id__in=competition.values('teams'), founder=request.user)
        if not user_teams.exists():
            messages.error(request, "You are not in this tournament")
            return redirect('singletournaments:list')
        else:
            competition = Competition.objects.get(id=pk)
            if not competition.bracket_generated:
                form.is_valid()
                if not form.cleaned_data['confirm']:
                    messages.error(request, "You submitted without confirming that you wanted to leave")
                    return redirect('singletournaments:leave', pk=pk)
                else:
                    user_team = Team.objects.get(id__in=competition.values('teams'), founder=request.user)
                    team = SingleEliminationTeam.objects.get(team_id=user_team.id, competition=competition)
                    team.delete()
                    competition.teams.remove(user_team)
                    team_users = user_team.players.all() | user_team.founder | user_team.captain.all() 
                    messages.success(request, "Gave %s credits to %s users" % (competition.req_credits, len(team_users)))
                    messages.success(request, "Left tournament %s" % competition.name)
                    return redirect('singletournaments:list')
            else:
                messages.error(request, "The bracket has been generated already, you cannot leave the tournament")
                return redirect('singletournaments:detail', pk=pk)


class SingleTournamentDetail(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = get_object_or_404(SingleEliminationCompetition, id=pk)
        ruleset = tournament.ruleset
        teams = tournament.teams.all()
        return render(request, 'singletournaments/singletournament_detail.html',
                      {'pk': pk, 'tournament': tournament, 'ruleset': ruleset, 'teams': teams})


class SingleTournamentTeamsList(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationCompetition.objects.get(id=pk)
        teams = tournament.teams.all
        return render(request, 'singletournaments/singletournament_teams.html',
                      {'x': pk, 'tournament': tournament, 'teams': teams})


class SingleTournamentBracket(View):

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        tournament = SingleEliminationCompetition.objects.get(id=pk)
        teams = tournament.teams.all()
        if tournament.bracket_generated:
            # show the right bracket
            rounds = SingleEliminationRound.objects.all().filter(tournament=tournament)
            return render(request, 'singletournaments/singletournament_bracket.html',
                          {'x': pk, 'tournament': tournament,
                           'teams': teams, 'rounds': rounds})
        else:
            # show some template that its not generated yet
            return render(request, 'singletournaments/no_bracket.html',
                          {'tournament': tournament})
