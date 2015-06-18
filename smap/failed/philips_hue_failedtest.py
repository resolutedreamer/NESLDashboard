#print "opening the philips_hue driver"
import os
from smap import actuate, driver
from smap.authentication import authenticated
#print "Importing HueInterface"
import HueInterface
print "philips_hue imports successful"

class lightbulb(driver.SmapDriver):
    """ Attempt to Access Philips Hue """
    def setup(self, opts):
	print "starting setup"
	print "opts values:"
	print opts
        self.IPAddress = os.path.expanduser(opts['IPAddress'])
	self.username = os.path.expanduser(opts['username'])

	# set up an appropriate actuator
        setup={'filename': opts.pop('Filename', '~/FileActuatorFile')}
        data_type = 'long'
        if not 'model' in opts or opts['model'] == 'binary':
            klass = BinaryActuator
        elif opts['model'] == 'discrete':
            klass = DiscreteActuator
            setup['states'] = opts.pop('states', ['cat', 'dog'])
        elif opts['model'] == 'continuous':
            klass = ContinuousActuator
            setup['range'] = map(float, opts.pop('range'))
            data_type = 'double'
        else:
            raise ValueError("Invalid actuator model: " + opts['model'])

	self.add_actuator('/point0', 'Switch Position',
                          klass, setup=setup, data_type=data_type, write_limit=5)

    def get_state(self, request):
        try:
            colors = HueInterface().getColors()
	    return colors
        except IOError:
            return None

    # @authenticated(['__has_ssl__'])
    def set_state(self, request, state):
        try:
	    newcolor = state
	    HueInterface().setColors(newcolor)
            colors = HueInterface().getColors()
	    return colors
        except IOError:
            return None

print "philips_hue class? successful"
