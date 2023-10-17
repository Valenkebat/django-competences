# Generated by Django 4.2.5 on 2023-10-06 13:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_remove_match_competition'),
        ('teams', '0001_initial'),
        ('profiles', '0001_initial'),
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoubleEliminationCompetition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='competitions.competition')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='League Ruleset', max_length=50)),
                ('ot_losses', models.BooleanField(default=True)),
                ('pts_ot_loss', models.PositiveSmallIntegerField(default=1)),
                ('ot_wins', models.BooleanField(default=False)),
                ('pts_ot_win', models.PositiveSmallIntegerField(default=3)),
                ('pts_win', models.PositiveSmallIntegerField(default=3)),
                ('pts_loss', models.PositiveSmallIntegerField(default=0)),
                ('allow_tie', models.BooleanField(default=False)),
                ('num_games', models.PositiveIntegerField(default=10)),
                ('auto_schedule', models.BooleanField(default=False)),
                ('auto_matchup', models.BooleanField(default=False)),
                ('num_divisions', models.PositiveSmallIntegerField(default=2)),
                ('max_division_size', models.PositiveSmallIntegerField(default=5)),
                ('allow_fa', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SingleEliminationCompetition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='competitions.competition')),
                ('current_round', models.SmallIntegerField(blank=True, default=1)),
                ('size', models.PositiveSmallIntegerField(choices=[(4, 4), (8, 8), (16, 16), (32, 32), (64, 64), (128, 128)], default=32)),
                ('xp_seed', models.BooleanField(default=False)),
                ('bracket_generated', models.BooleanField(default=False)),
                ('prize1', models.CharField(default='no prize specified', max_length=50)),
                ('prize2', models.CharField(default='no prize specified', max_length=50)),
                ('prize3', models.CharField(default='no prize specified', max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='tournament_images')),
                ('disable_userreport', models.BooleanField(default=True)),
                ('map_pool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='map_pool', to='matches.mappoolchoice')),
                ('second', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secondplaceteam', to='teams.team')),
                ('teams', models.ManyToManyField(blank=True, to='teams.team')),
                ('third', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thirdplaceteam', to='teams.team')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winningteam', to='teams.team')),
            ],
        ),
        migrations.RemoveField(
            model_name='competition',
            name='text',
        ),
        migrations.AddField(
            model_name='competition',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='competition',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competition',
            name='info',
            field=models.TextField(default='No information provided'),
        ),
        migrations.AddField(
            model_name='competition',
            name='teamformat',
            field=models.SmallIntegerField(choices=[(0, '1v1'), (1, '2v2'), (2, '3v3'), (3, '4v4')], default=1),
        ),
        migrations.AddField(
            model_name='competition',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='name',
            field=models.CharField(default='Competition Name', max_length=50),
        ),
        migrations.CreateModel(
            name='SingleEliminationTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seed', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actualteam', to='teams.team')),
                ('tournament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intournament', to='competitions.singleeliminationcompetition')),
            ],
        ),
        migrations.CreateModel(
            name='SingleEliminationRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roundnum', models.PositiveSmallIntegerField(default=1)),
                ('matchesnum', models.PositiveSmallIntegerField(default=2)),
                ('info', models.TextField(default='No info specified')),
                ('matches', models.ManyToManyField(to='matches.match')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withtournamentround', to='competitions.singleeliminationcompetition')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.PositiveSmallIntegerField(default=0)),
                ('losses', models.PositiveSmallIntegerField(default=0)),
                ('ot_losses', models.PositiveSmallIntegerField(default=0)),
                ('ot_wins', models.PositiveSmallIntegerField(default=0)),
                ('ties', models.PositiveSmallIntegerField(default=0)),
                ('points', models.PositiveIntegerField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='league_team', to='teams.team')),
            ],
            options={
                'ordering': ['-points'],
            },
        ),
        migrations.CreateModel(
            name='LeagueFreeAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='Include information about Free Agent here')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fa_profile', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueDivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('matches', models.ManyToManyField(blank=True, to='matches.match')),
                ('teams', models.ManyToManyField(blank=True, to='competitions.leagueteam')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueCompetition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='competition', to='competitions.competition')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('preseason', 'Preseason'), ('regular season', 'Regular Season'), ('playoffs', 'Playoffs'), ('finals', 'Finals'), ('offseason', 'Offseason')], default='preseason', max_length=50)),
                ('allow_register', models.BooleanField(default=False)),
                ('open_register', models.DateTimeField()),
                ('close_register', models.DateTimeField()),
                ('start', models.DateTimeField()),
                ('req_credits', models.PositiveSmallIntegerField(default=0)),
                ('size', models.PositiveSmallIntegerField(default=8)),
                ('disable_userreport', models.BooleanField(default=False)),
                ('divisions', models.ManyToManyField(blank=True, to='competitions.leaguedivision')),
                ('fa', models.ManyToManyField(blank=True, related_name='league_fas', to='competitions.leaguefreeagent')),
                ('featured_matches', models.ManyToManyField(blank=True, related_name='featured_matches', to='matches.match')),
                ('featured_players', models.ManyToManyField(blank=True, related_name='featured_players', to='matches.match')),
                ('maps', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='league_maps', to='matches.mappoolchoice')),
                ('non_conference', models.ManyToManyField(blank=True, related_name='non_conference_matches', to='matches.match')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='league_settings', to='competitions.leaguesettings')),
                ('teams', models.ManyToManyField(blank=True, to='competitions.leagueteam')),
            ],
        ),
    ]