from django.db import models
from django.conf import settings


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
        ('exercise', 'Exercise'),
        ('break', 'Break time'),
    ]
    kind = models.CharField(choices=types, max_length=8, default='exercise')  # either a full exercise or a break time
    duration = models.PositiveIntegerField(default=30)
    plan = models.ForeignKey(to=Workout, on_delete=models.CASCADE)  # An exercise relates to its plan
    preptime = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField()

    objects = models.Manager()

    @classmethod
    def check_permission(cls, request):
        ids = tuple(map(lambda x: int(x), request.POST.getlist('exrs[]')))
        selected_exrs = cls.objects.filter(id__in=ids)
        db_exrs = cls.objects.filter(owner=...)
        ownage_checked = all(map(lambda x: x.plan.owner == request.user, selected_exrs))
        if len(ids) == selected_exrs.count() and ownage_checked:
            ...

    def save(self, *args, **kwargs):
        if self.order is None:
            existing = self.__class__.objects.filter(plan=self.plan)
            self.order = existing.count()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Exercise("{self.name}", plan:{self.plan})'