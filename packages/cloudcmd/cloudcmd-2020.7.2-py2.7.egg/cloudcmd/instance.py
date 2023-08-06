from cliff.lister import Lister

class InstanceList(Lister):
    """List orders."""

    def get_parser(self, prog_name):
        parser = super(InstanceList, self).get_parser(prog_name)
        parser.add_argument('--limit', '-l', default=10,
                            help='specify the limit to the number of items '
                                 'to list per page (default: %(default)s; '
                                 'maximum: 100)',
                            type=int)
        return parser

    def take_action(self, args):
	instances = self.app.cloud_obj.compute.list_instances()
        return (('ID', 'Name', 'Public-IP', 'Size', 'State', 'Image-Name' ),
                ((instance.oid, instance.name, instance.public_ip, instance.size, instance.state, instance.image_name) for instance in instances)
                )

from cliff.show import ShowOne

class InstanceShow(ShowOne):
	"""Show Instance information."""
	def get_parser(self, prog_name):
        	parser = super(InstanceShow, self).get_parser(prog_name)
        	parser.add_argument('instance_id', help='The instance id.')
        	return parser

	def take_action(self, args):
		instance = self.app.cloud_obj.compute.get_instance_by_id(args.instance_id)

		return (('ID', 'Name', 'Size', 'State', 'Keypair', 'User-ID', 'User-Name', 'Project-ID', 'Project-Name', 'Image-ID', 'Image-Name', 'Public-IP', 'Private-IP', 'Availability-Zone', 'Hypervisor-Name', 'Port-ID', 'Mac-Addr', 'Network-Id'), (instance.id, instance.name, instance.size, instance.state, instance.keypair_name,  instance.user_id, instance.user_name, instance.tenant_id, instance.tenant_name, instance.image_id, instance.image_name, instance.public_ip, instance.private_ip, instance.availability_zone, instance.hypervisor_name, instance.port_id, instance.mac_id, instance.network_id))

from cliff.command import Command

class InstancesSensu(Command):
    """sensu alert for instances"""

    def take_action(self, parsed_args):
	instances = self.app.cloud_obj.compute.list_instances()
	count = 0
	msg = ''
	for instance in instances:
		if instance.state == 'ERROR':
			count += 1
			msg += '[Id:{} Name:{} user:{} tenant:{}] '.format(instance.id, instance.name, instance.user_name, instance.tenant_name)

	if count == 0:
		return 'OK'
	
	raise Exception('{} instance(s) in Error state. {}'.format(count, msg))
	
