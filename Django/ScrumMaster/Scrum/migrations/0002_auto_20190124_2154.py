# Generated by Django 2.1.2 on 2019-01-24 20:54

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Scrum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatscrumSlackApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SLACK_VERIFICATION_TOKEN', models.CharField(blank=True, max_length=80, null=True)),
                ('CLIENT_ID', models.CharField(blank=True, max_length=80, null=True)),
                ('CLIENT_SECRET', models.CharField(blank=True, max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScrumGoalHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('status', models.IntegerField(default=-1)),
                ('goal_project_id', models.IntegerField(default=0)),
                ('hours', models.IntegerField(default=-1)),
                ('time_created', models.DateTimeField()),
                ('file', models.ImageField(blank=True, null=True, upload_to='')),
                ('done_by', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ScrumSlack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=500)),
                ('team_name', models.CharField(max_length=500)),
                ('team_id', models.CharField(max_length=500)),
                ('channel_id', models.CharField(max_length=500)),
                ('access_token', models.CharField(max_length=500)),
                ('bot_user_id', models.CharField(max_length=500)),
                ('bot_access_token', models.CharField(max_length=500)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scrum.ScrumChatRoom')),
                ('scrumproject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scrum.ScrumProject')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='scrumgoal',
            name='file',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media'), upload_to=''),
        ),
        migrations.AddField(
            model_name='scrumuser',
            name='slack_email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='scrumuser',
            name='slack_user_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='scrumgoalhistory',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scrum.ScrumGoal'),
        ),
        migrations.AddField(
            model_name='scrumgoalhistory',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scrum.ScrumProject'),
        ),
        migrations.AddField(
            model_name='scrumgoalhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Scrum.ScrumProjectRole'),
        ),
    ]
