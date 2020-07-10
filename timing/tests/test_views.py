from django.test import TestCase
from django.shortcuts import reverse
from django.test import Client

username, password = 'odmen', 'odmen'


class GeneralApiTest(TestCase):
    fixtures = ['user_test_fixture.json', 'wrk_test_fixture.json', 'exr_test_fixture.json']

    def setUp(self):
        self.client = Client()
        self.client.post(reverse('users:login'), {'username': username, 'password': password})

    def test_homepage(self):
        response = self.client.get(reverse('timing:home_page'))
        self.assertEqual(response.status_code, 200)

    def test_workout_list(self):
        # show all workouts
        show_wrk_resp = self.client.get(reverse('timing:show_workouts'))
        self.assertEqual(show_wrk_resp.status_code, 200)
        # details with exrs
        wrk_detail_resp = self.client.get(reverse('timing:workout_detail', args=[1]))
        self.assertEqual(wrk_detail_resp.status_code, 200)
        self.assertContains(wrk_detail_resp, "Exercise A")
        # details empty
        wrk_detail_resp_empty = self.client.get(reverse('timing:workout_detail', args=[2]))
        self.assertEqual(wrk_detail_resp_empty.status_code, 200)
        self.assertContains(wrk_detail_resp_empty, "Nothing here yet")

    def test_play_timer(self):
        timer_resp = self.client.get(reverse('timing:play_timer', args=[1]))
        self.assertEqual(timer_resp.status_code, 200)
        self.assertContains(timer_resp, "Exercise A")
