from django.db import models, router
from django.conf import settings
from django.db.models.deletion import Collector
from django.shortcuts import get_object_or_404


class Workout(models.Model):
    '''Represents a full workout'''

    name = models.CharField(max_length=64)
    warmup_time = models.PositiveIntegerField(default=0)
    cooldown_time = models.PositiveIntegerField(default=0)
    laps = models.PositiveIntegerField(default=1)  # TODO: constraint > 0
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f'Workout("{self.name}", id_{self.id})'


class Exercise(models.Model):
    '''Represents a single exercise'''

    name = models.CharField(max_length=42)
    types = [
        ('break', 'Break time'),
        ('exercise', 'Exercise'),
    ]
    kind = models.CharField(choices=types, max_length=8, default='exercise')  # either a full exercise or a break time
    duration = models.PositiveIntegerField(default=30)
    plan = models.ForeignKey(to=Workout, on_delete=models.CASCADE)  # An exercise relates to its plan
    preptime = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField()

    objects = models.Manager()

    @classmethod
    def check_permission(cls, request, ids):
        '''Checks whether the received ids are valid or not'''
        selected_exrs = cls.objects.filter(id__in=ids)
        wrk_id = request.POST.get('wrk_id')
        main_workout = get_object_or_404(Workout, id=wrk_id)
        main_count = main_workout.exercise_set.count()
        ownage_checked = all(map(lambda exr: exr.plan.owner == request.user, selected_exrs))
        if len(ids) == main_count == selected_exrs.count() and ownage_checked and len(ids) != 0:
            return True, selected_exrs
        return False, cls.objects.none()

    def delete(self, using=None, keep_parents=False):  # rewriting delete method for correct exr representation
        using = using or router.db_for_write(self.__class__, instance=self)
        assert self.pk is not None, (
                "%s object can't be deleted because its %s attribute is set to None." %
                (self._meta.object_name, self._meta.pk.attname)
        )
        collector = Collector(using=using)
        collector.collect([self], keep_parents=keep_parents)
        for_changing = self.__class__.objects.filter(order__gte=self.order)  # __gte required for correct order saving
        del_result = collector.delete()
        for exr in for_changing:
            exr.order -= 1
            exr.save()
        return del_result

    def save(self, *args, **kwargs):
        if self.order is None:
            existing = self.__class__.objects.filter(plan=self.plan)
            self.order = existing.count()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Exercise("{self.name}", plan:{self.plan}, order:{self.order})'