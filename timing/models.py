from django.db import models


class Workout(models.Model):
    '''Represents a full worout'''

    name = models.CharField(default='My Workout', max_length=120)
    warmup_time = models.IntegerField(default=0)
    cooldown_time = models.IntegerField(default=0)
    laps = models.IntegerField(default=1)


class AbstractExercise(models.Model):
    '''Base abstract class for an exercise'''

    duration = models.IntegerField(default=30)
    plan = models.ForeignKey(to=Workout, on_delete=models.CASCADE)  # An exercise relates to its plan
    order = models.IntegerField(null=True)  # exercise order in the self-made list (workout)
    # One must set boolean class attribute "active" in child class...

    @classmethod
    def add_exr(cls, n=None, **params):
        '''Adds one exercise with params and order n'''
        cur_set = cls.objects.filter(plan=params['plan'])
        if n is None:
            n = cur_set.count()
            cls.objects.create(order=n,**params)
        else:
            sliced_set = cur_set.filter(n__gt=n).order_by('-order')
            for inst in sliced_set:
                inst.order += 1
            cls.objects.create(order=n, **params)

    @classmethod
    def del_exr(cls, plan_id, n=None):
        '''Deletes an exercise of order n from a particular plan'''
        cur_set = cls.objects.filter(plan=plan_id)
        if n is None:
            n = cur_set.count() - 1
            cls.objects.delete(order=n, plan=plan_id)
        else:
            sliced_set = cur_set.filter(order__gt=n).order_by('order')
            cls.objects.delete(order=n, plan=plan_id)
            for inst in sliced_set:
                inst.order -= 1

    @classmethod
    def move_exr(cls, plan_id, n_start, offset):
        cur_exr = cls.objects(plan=plan_id, order=n_start)
        cur_set = cls.objects.filter(plan=plan_id)
        count = cur_set.count()
        offset = min(max(offset, -n_start), count-n_start)
        if offset > 0:
            sliced_set = cur_set.filter(order__gt=n_start, order__lt=n_start+offset+1).order_by('order')
            for exr in sliced_set:
                exr.order -= 1
        elif offset < 0:
            sliced_set = cur_set.filter(order__gt=n_start-offset-1, order__lt=n_start).order_by('order')
            for exr in sliced_set:
                exr.order += 1
        else:
            raise Exception
        cur_exr.order = n_start + offset


    class Meta:
        abstract = True
        ##unique_together = ('plan', 'order')


class Exercise(AbstractExercise):
    '''Represents a single exercise'''

    name = models.CharField(default='Exercise', max_length=63)
    preptime = models.IntegerField(null=True, blank=True)
    FOR_REPS = 'for_reps'
    FOR_TIME = 'for_time'
    exercise_types = [
        (FOR_REPS, 'for reps'),
        (FOR_TIME, 'for time'),
        ]
    exr_type = models.CharField(choices=exercise_types, max_length=8)
    active = True


class Break(AbstractExercise):
    '''Represents a break time'''

    name = models.CharField(default='Break', max_length=63)
    active = False