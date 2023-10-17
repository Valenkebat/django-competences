from django import forms

from competitions.models import Competition
from teams.models import Team, TeamInvite
from profiles.models import UserProfile


class CompetitionCreateForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name','competition_type']

    
class CompetitionJoinGet(forms.ModelForm):
    teams = forms.ModelChoiceField(queryset=None)

    # tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())

    class Meta:
        model = Competition
        fields = ()

    def __init__(self, request, *args, **kwargs):
        self.username = request.user
        #invites = TeamInvite.objects.filter(hasPerms=True, user_id=self.username.id)
        profile = UserProfile.objects.get(user=request.user)
        teams = profile.captain_teams | profile.founder_teams
        #team = Team.objects.filter(id__in=invites.values_list('team', flat=True))
        super().__init__(*args, **kwargs)
        self.fields['teams'].widget.attrs.update({'name': 'teams', 'class': 'form-control'})
        self.fields['teams'].queryset = teams


class CompetitionJoinPost(forms.ModelForm):
    teams = forms.ModelChoiceField(queryset=Team.objects.all())

    # tournaments = forms.ModelChoiceField(queryset=SingleEliminationTournament.objects.all())

    class Meta:
        model = Competition
        fields = ()


class CompetitionSort(forms.Form):
    
    def __init__(self, *args, **kwargs):

        super(CompetitionSort, self).__init__(*args, **kwargs)



class CompetitionLeaveForm(forms.Form):
    confirm = forms.BooleanField(required=False)

    class Meta:
        fields = 'Confirm'