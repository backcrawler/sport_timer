# Generated by Django 2.2.10 on 2020-07-02 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('warmup_time', models.PositiveIntegerField(default=0)),
                ('cooldown_time', models.PositiveIntegerField(default=0)),
                ('laps', models.PositiveIntegerField(default=1)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('kind', models.CharField(choices=[('exercise', 'Exercise'), ('break', 'Break')], default='exercise', max_length=8)),
                ('duration', models.PositiveIntegerField(default=30)),
                ('preptime', models.IntegerField(default=0)),
                ('order', models.PositiveIntegerField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timing.Workout')),
            ],
        ),
    ]
