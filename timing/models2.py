from django.db import models
from itertools import chain


class Workout(models.Model):
    '''Represents a full workout'''

    name = models.CharField(default='My Workout', max_length=120)
    warmup_time = models.IntegerField(default=0)
    cooldown_time = models.IntegerField(default=0)
    laps = models.IntegerField(default=1)


class Exercise(models.Model):
    '''Represents a single exercise'''

    duration = models.IntegerField(default=30)
    plan = models.ForeignKey(to=Workout, on_delete=models.CASCADE)  # An exercise relates to its plan
    order = models.IntegerField(null=True)  # exercise order in the self-made list (workout)
    preptime = models.IntegerField(null=True, blank=True)

    @classmethod
    def add_exr(cls, n=None, **params):
        '''Adds one exercise with params and order n'''
        cur_set = cls.objects.filter(plan=params['plan'])
        if n is None:
            n = cur_set.count()
            cls.objects.create(order=n, **params)
        else:
            sliced_set = cur_set.filter(n__gt=n).order_by('-order')
            for inst in sliced_set:
                inst.order += 1
            cls.objects.create(order=n, **params)

    @classmethod
    def del_exr(cls, plan_inst, n=None):
        '''Deletes an exercise of order n from a particular plan'''
        cur_set = cls.objects.filter(plan=plan_inst)
        if n is None:
            n = cur_set.count() - 1
            cls.objects.delete(order=n, plan=plan_inst)
        else:
            sliced_set = cur_set.filter(order__gt=n).order_by('order')
            cls.objects.delete(order=n, plan=plan_inst)
            for inst in sliced_set:
                inst.order -= 1

    @classmethod
    def move_exr(cls, plan_inst, n_start, offset):
        cur_exr = cls.objects(plan=plan_inst, order=n_start)
        cur_set = cls.objects.filter(plan=plan_inst)
        count = cur_set.count()
        offset = min(max(offset, -n_start), count - n_start)
        if offset > 0:
            sliced_set = cur_set.filter(order__gt=n_start, order__lt=n_start + offset + 1).order_by('order')
            for exr in sliced_set:
                exr.order -= 1
        elif offset < 0:
            sliced_set = cur_set.filter(order__gt=n_start - offset - 1, order__lt=n_start).order_by('order')
            for exr in sliced_set:
                exr.order += 1
        else:
            raise Exception
        cur_exr.order = n_start + offset