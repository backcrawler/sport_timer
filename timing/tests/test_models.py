from django.test import TestCase
from django.contrib.auth.models import User

from timing.models import Exercise, Workout


class DummyRequest:

    class Inner:
        '''Empty class for further imitations'''
        pass

    def __init__(self, usr, wrk_id):
        self.user = usr
        self.wrk_id = wrk_id
        self.POST = self.Inner()
        self.POST.get = lambda x: self.wrk_id


class CoreModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser', email='van@gmail.com', password='522228xXx')
        self.wrk = Workout.objects.create(name='Test Wrk', owner=self.user)

    def test_main(self):
        self.assertEqual(Workout.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        exr1 = Exercise.objects.create(name='Exr1', duration=10, kind='break', plan=self.wrk)
        exr2 = Exercise.objects.create(name='Exr2', plan=self.wrk)
        exr3 = Exercise.objects.create(name='Exr3', plan=self.wrk)
        exr4 = Exercise.objects.create(name='Exr4', plan=self.wrk)
        self.assertEqual(Exercise.objects.count(), 4)
        self.assertEqual(exr1.order, 0)
        self.assertEqual(exr4.order, 3)
        self.assertEqual(exr2.kind, 'exercise')
        self.assertEqual(exr2.duration, 30)
        exr3.delete()
        new4 = Exercise.objects.filter(name='Exr4').first()
        self.assertEqual(new4.order, 2)

    def test_check_permission(self):
        exrs = []
        for _ in range(5):
            current_exr = Exercise.objects.create(name='Exr1', plan=self.wrk)
            exrs.append(current_exr)
        # 1st check
        req = DummyRequest(self.user, self.wrk.id)
        ids = tuple(exr.id for exr in exrs)
        valid_flag, _ = Exercise.check_permission(req, ids)
        self.assertEqual(valid_flag, True)
        # 2d check
        self.user2 = User.objects.create_user(username='newUser', email='pan@gmail.com', password='522228xXx')
        req2 = DummyRequest(self.user2, self.wrk.id)
        ids2 = tuple(exr.id for exr in exrs)
        invalid_flag, _ = Exercise.check_permission(req2, ids2)
        self.assertEqual(invalid_flag, False)
        # 3d check
        req3 = DummyRequest(self.user, self.wrk.id)
        ids3 = list(exr.id for exr in exrs) + [1]
        invalid_flag, _ = Exercise.check_permission(req3, ids3)
        self.assertEqual(invalid_flag, False)
        # 4th check
        req4 = DummyRequest(self.user, self.wrk.id)
        ids4 = list(exr.id for exr in exrs)
        ids4.pop()
        invalid_flag, _ = Exercise.check_permission(req4, ids4)
        self.assertEqual(invalid_flag, False)
        # 5th check
        req5 = DummyRequest(self.user, self.wrk.id)
        ids5 = list(exr.id for exr in exrs)
        ids5[0] = ids5[0]*10
        invalid_flag, _ = Exercise.check_permission(req5, ids5)
        self.assertEqual(invalid_flag, False)