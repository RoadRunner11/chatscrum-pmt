# Generated by Django 2.0.7 on 2020-04-25 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Scrum', '0022_auto_20200425_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatslack',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Scrum.ScrumProject'),
        ),
    ]