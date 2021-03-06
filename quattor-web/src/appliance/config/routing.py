"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/', controller='appliance', action='status')
    map.connect('/about', controller='appliance', action='about')

    map.connect('/commands', controller='forms', action='index')
    map.connect('/form/{cmd}', controller='forms', action='generate_form',
                conditions=dict(method=['GET']))
    map.connect('/form/{cmd}', controller='forms', action='process_form',
                conditions=dict(method=['POST']))

    map.connect('/sandboxes', controller='appliance', action='sandboxes')

    map.connect('/appliance/log/{log}', controller='appliance', action='log')

    map.connect('/appliance/krb5settings', controller='appliance', action='krb5display')
    map.connect('/appliance/krb5configure', controller='appliance', action='krb5configure')

    map.connect('/warehouse/update', controller='warehouse', action='upload',
                conditions=dict(method=['POST']))

    return map
