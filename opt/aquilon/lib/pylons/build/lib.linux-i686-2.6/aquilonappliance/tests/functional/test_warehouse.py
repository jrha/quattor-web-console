from aquilonappliance.tests import *

class TestWarehouseController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='warehouse', action='index'))
        # Test response...
