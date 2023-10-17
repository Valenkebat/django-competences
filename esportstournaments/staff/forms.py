from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from matches.models import Match, MapChoice, MapPoolChoice
from news.models import Post
from pages.models import StaticInfo, SocialInfo, Partner, FrontPageSlide, CoreSetting, StaticPage
from profiles.models import UserProfile
from competitions.models import Competition, SingleEliminationCompetition, SingleEliminationRound
from support.models import TicketComment, Ticket, TicketCategory, QuestionAnswerCategory, QuestionAnswer
from teams.models import Team, RosterRole
from competitions.models import LeagueCompetition, LeagueSettings, LeagueDivision, LeagueFreeAgent


class StaticInfoForm(forms.ModelForm):
    class Meta:
        model = StaticInfo
        fields = '__all__'


class SocialInfoForm(forms.ModelForm):
    twitchchannel = forms.URLField(required=False)
    youtubechannel = forms.URLField(required=False)
    twitterprofile = forms.URLField(required=False)
    facebookpage = forms.URLField(required=False)
    instagrampage = forms.URLField(required=False)

    class Meta:
        model = SocialInfo
        fields = '__all__'


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'


class SingleRulesetCreateForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ('name', 'info')


class TicketSearchForm(forms.Form):
    showClosed = forms.BooleanField(required=False, label='Show closed')
    searchQuery = forms.CharField(required=False, label='Search')


class TicketCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = TicketCategory
        fields = ('name', 'priority',)


class TicketCommentCreateForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ('comment',)


class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = SingleEliminationCompetition
        fields = '__all__'
        widgets = {
            'open_register': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'}),
            'close_register': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker2',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker2'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker3',
                                                'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker3'})
        }

    def __init__(self, *args, **kwargs):
        super(CreateTournamentForm, self).__init__(*args, **kwargs)
        self.fields['twitch'].required = False


class EditTournamentForm(forms.ModelForm):

    class Meta:
        model = SingleEliminationCompetition
        fields = '__all__'
        widgets = {
            'open_register': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'}),
            'close_register': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker2',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker2'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker3',
                                                'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker3'})
        }

    def __init__(self, *args, **kwargs):
        super(EditTournamentForm, self).__init__(*args, **kwargs)
        self.fields['twitch'].required = False


class AddTournamentTeamForm(forms.ModelForm):
    teams = forms.IntegerField()

    class Meta:
        model = SingleEliminationCompetition
        fields = ()


class DeclareMatchWinnerForm(forms.ModelForm):
    winner = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Match
        # fields = ('winner',)
        fields = ()

    def __init__(self, request, pk, *args, **kwargs):
        match = Match.objects.filter(id=pk)
        team1 = Team.objects.filter(id__in=match.values_list('hometeam', flat=True))
        team2 = Team.objects.filter(id__in=match.values_list('awayteam', flat=True))
        super().__init__(*args, **kwargs)
        self.fields['winner'].queryset = team1 | team2


class DeclareMatchWinnerPost(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('winner', 'completed')


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'slug', 'body', 'publish', 'status')
        widgets = {
            'publish': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'}),

        }


class TicketStatusChangeForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('status', 'assignee')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assignees = User.objects.filter(Q(user__user_type='admin') | Q(user__user_type='superadmin'))
        self.fields['assignee'].queryset = assignees


class DeclareTournamentWinnerForm(forms.ModelForm):
    class Meta:
        model = SingleEliminationCompetition
        fields = ('winner', 'second', 'third')


class CreateNewsPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class EditNewsPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'publish': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'}),
        }


class RemovePlayerForm(forms.Form):
    remove = forms.ModelChoiceField(queryset=None)

    def __init__(self, request, pk, *args, **kwargs):
        team = Team.objects.get(id=pk)
        players = team.players.all() | team.captain.all()
        super().__init__(*args, **kwargs)
        self.fields['remove'].queryset = players


class RemovePlayerFormPost(forms.Form):
    remove = forms.ModelChoiceField(queryset=None)


class ModifyUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('xp', 'user_type', 'alternate_name','steamid64', 'discord')




class EditMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('info', 'disable_userreport', 'bestof', 'server', 'datetime', 'map_pool', 'maps')
        widgets = {
            'datetime': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'})}




class EditRoundInfoForm(forms.ModelForm):
    class Meta:
        model = SingleEliminationRound
        fields = ('info',)


class MapChoiceForm(forms.ModelForm):
    class Meta:
        model = MapChoice
        fields = '__all__'


class MapPoolChoiceForm(forms.ModelForm):
    class Meta:
        model = MapPoolChoice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MapPoolChoiceForm, self).__init__(*args, **kwargs)
        self.fields['maps'].widget = forms.widgets.CheckboxSelectMultiple()
        if hasattr(self.instance, 'game'):
            self.fields['maps'].queryset = MapChoice.objects.filter(game_id=self.instance.game)


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'founder', 'country', 'players')


class CreateQuestionAnswerCategory(forms.ModelForm):
    class Meta:
        model = QuestionAnswerCategory
        fields = ('name',)


class CreateQuestionAnswer(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ('question', 'answer', 'category')


class CreateSlide(forms.ModelForm):
    class Meta:
        model = FrontPageSlide
        fields = '__all__'


class CreateLeagueForm(forms.ModelForm):

    class Meta:
        model = LeagueCompetition
        fields = '__all__'
        widgets = {
            'open_register': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker1',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker1'}),
            'close_register': forms.DateTimeInput(
                attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker2',
                       'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker2'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'id': 'datetimepicker3',
                                                'data-toggle': 'datetimepicker', 'data-target': '#datetimepicker3'})
        }

        exclude = ('non_conference',)


class TeamForceAddUser(forms.Form):
    user = forms.CharField(required=True, max_length=50)


class CreateLeagueSettingsForm(forms.ModelForm):
    class Meta:
        model = LeagueSettings
        fields = '__all__'


class EditLeagueSettingsForm(forms.ModelForm):
    class Meta:
        model = LeagueSettings
        fields = '__all__'


class AddLeagueMatchForm(forms.Form):
    awayteam = forms.IntegerField(required=True)
    hometeam = forms.IntegerField(required=True)
    division = forms.IntegerField(required=False)

    class Meta:
        fields = ('hometeam', 'awayteam', 'division')


class DivisionAddTeamForm(forms.Form):
    teamid = forms.IntegerField(required=True)

    class Meta:
        fields = ('teamid',)


class CreateOllySetting(forms.ModelForm):
    class Meta:
        model = CoreSetting
        fields = '__all__'


class CreateTeamRosterRole(forms.ModelForm):
    class Meta:
        model = RosterRole
        fields = '__all__'


class StaticPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = '__all__'
