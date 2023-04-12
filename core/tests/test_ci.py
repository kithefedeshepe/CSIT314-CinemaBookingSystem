from django.test import SimpleTestCase
class TestCI(SimpleTestCase):
    def test_ci_setup(self):
        assert(1 == 1)