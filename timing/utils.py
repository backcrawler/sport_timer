from django.db.models.signals import post_delete, post_save
from django.core.signals import request_finished
from django.dispatch import receiver
from timing.models import Workout, Exercise


def save_post(sender, instance, *args, **kwargs):
    print(f'{sender.__name__} instance was just saved')


def del_post(sender, instance, *args, **kwargs):
    print(f'{sender.__name__} instance was just deleted')


post_save.connect(save_post, sender=Workout)
post_delete.connect(del_post, sender=Workout)

# alternative version with receiver decorator
@receiver(request_finished)
def req_fin_callback(sender, **kwargs):
    print('Request finished')