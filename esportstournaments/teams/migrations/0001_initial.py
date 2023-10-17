# Generated by Django 4.2.5 on 2023-10-02 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RosterRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unknown', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('tag', models.CharField(max_length=10, null=True)),
                ('about_us', models.CharField(blank=True, default='Forever a mystery', max_length=250)),
                ('website', models.CharField(blank=True, default='No Website', max_length=100)),
                ('twitter', models.CharField(blank=True, default='None Linked', max_length=15)),
                ('twitch', models.CharField(blank=True, default='None Linked', max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('num_matchloss', models.SmallIntegerField(default=0)),
                ('num_matchwin', models.SmallIntegerField(default=0)),
                ('num_tournywin', models.SmallIntegerField(default=0)),
                ('numtournyloss', models.SmallIntegerField(default=0)),
                ('totalxp', models.PositiveSmallIntegerField(default=0)),
                ('rank', models.PositiveSmallIntegerField(default=100)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('image', models.ImageField(blank=True, upload_to='team_images')),
                ('captain', models.ManyToManyField(blank=True, related_name='teamcaptain', to=settings.AUTH_USER_MODEL)),
                ('founder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='founder', to=settings.AUTH_USER_MODEL)),
                ('matches', models.ManyToManyField(blank=True, related_name='team_matches', to='matches.match')),
                ('players', models.ManyToManyField(blank=True, related_name='teamplayers', to=settings.AUTH_USER_MODEL)),
                ('team_stat', models.ManyToManyField(blank=True, related_name='match_team_stat', to='matches.teammatchstats')),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='TeamInvite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire', models.DateTimeField()),
                ('captain', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('declined', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frominvite', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitedto', to='teams.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toinvite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RosterMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined', models.DateTimeField(auto_created=True)),
                ('description', models.TextField(default='No Description')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rostermemberrole', to='teams.rosterrole')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rostermemberuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('members', models.ManyToManyField(to='teams.rostermember')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamroster', to='teams.team')),
            ],
        ),
    ]
