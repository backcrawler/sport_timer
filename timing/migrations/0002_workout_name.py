# Generated by Django 3.0.3 on 2020-03-01 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='name',
            field=models.CharField(default='My Workout', max_length=120),
        ),
    ]
