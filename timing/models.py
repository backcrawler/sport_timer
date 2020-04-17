from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Workout(models.Model):
    '''Represents a full workout'''

    name = models.CharField(default='My Workout', max_length=120)
    warmup_time = models.IntegerField(default=0)
    cooldown_time = models.IntegerField(default=0)
    laps = models.IntegerField(default=1)
    exrs = ArrayField(models.IntegerField(), default=list)
    date_added = models.DateTimeField(auto_now_add=True)  # TODO: date_added
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Workout("{self.name}", id_{self.id})'


class Exercise(models.Model):
    '''Represents a single exercise'''

    name = models.CharField(default='Exercise', max_length=63)
    duration = models.IntegerField(default=30)
    plan = models.ForeignKey(to=Workout, on_delete=models.CASCADE)  # An exercise relates to its plan
    preptime = models.IntegerField(default=0)

    @classmethod
    def add_exr(cls, **params):
        '''Adds one exercise with params'''
        obj = cls.objects.create(**params)
        ##obj.save()
        obj.plan.exrs.append(obj.id)
        obj.plan.save()

    def del_exr(self):
        '''Deletes an exercise from a particular plan'''
        plan = self.plan
        plan.exrs.remove(self.id)
        plan.save()
        self.delete()

    def move_exr(self, offset):
        plan = self.plan
        array = plan.exrs
        idx = array.index(self.id)
        offset = min(max(offset, -idx), len(array) - idx)
        array.insert(idx+offset, array.pop(idx))
        plan.save()

    def __str__(self):
        return f'Exercise("{self.name}", id_{self.id})'