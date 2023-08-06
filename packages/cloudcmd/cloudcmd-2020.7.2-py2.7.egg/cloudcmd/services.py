from cliff.lister import Lister

class ServicesList(Lister):
    """List services."""

    def take_action(self, args):
	services = self.app.cloud_obj.services.list_services()
        return (('ID', 'Name', 'Status', 'State', 'Host' ),
                ((service.id, service.name, service.status, service.state, service.host) for service in services))


from cliff.command import Command

class ServicesSensu(Command):
    """sensu alert for services"""

    def take_action(self, parsed_args):
	services = self.app.cloud_obj.services.list_services()
	count = 0
        msg = ''
	for service in services:
		if service.status == 'disabled' or  service.state == 'down':
			count += 1
		 	msg += '[Name:{} State:{} Status:{} Host:{}]'.format(service.name, service.state, service.status, service.host)
			

	if count == 0:
		return 'OK'
	
	raise Exception('{} service(s) in down/disabled state. {}'.format(count, msg))
