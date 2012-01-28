from aquilonappliance.tests import *

class TestAquilonController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='aquilon', action='index'))
        # Test response...
