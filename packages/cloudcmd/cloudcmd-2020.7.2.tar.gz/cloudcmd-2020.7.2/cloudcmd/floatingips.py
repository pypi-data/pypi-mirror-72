from cliff.lister import Lister

class FloatingipsList(Lister):
    """List Floating ips"""

    def take_action(self, args):
	floating_ips = self.app.cloud_obj.networks.list_floating_ips()
        return (('ID', 'Public-IP', 'Private-IP', 'State', 'Port-ID', 'Tenant-Name', 'Tenant-ID' ),
                ((f.id, f.floating_ip_address, f.fixed_ip_address, f.state, f.nic_id, f.tenant_name, f.id) for f in floating_ips))

from cliff.show import ShowOne

class FloatingipShow(ShowOne):
	"""Show floating ip  information."""
	def get_parser(self, prog_name):
        	parser = super(FloatingipShow, self).get_parser(prog_name)
        	parser.add_argument('floatingip_id', help='The floating ip id.')
        	return parser

	def take_action(self, args):
		f = self.app.cloud_obj.networks.get_floating_ip_by_id(args.floatingip_id)

		return (('ID', 'Public-IP', 'Private-IP', 'State', 'Port-ID', 'Network-ID', 'Tenant-ID'), (f.id, f.floating_ip_address, f.fixed_ip_address, f.state, f.nic_id, f.network_id, f.tenant_id))

class FloatingipSummary(ShowOne):
	"""Show Total, free, alloacted, unallocated floating ips."""
	def take_action(self, args):
		total  = self.app.cloud_obj.networks.total_floating_ips
		ips = self.app.cloud_obj.networks.list_floating_ips()
		allocated = unallocated = 0
		for ip in ips:
			if ip.state == 'up':
				allocated += 1
			elif ip.state == 'down':
				unallocated += 1
			else: 
				pass
		
		free = total - len(ips)
		return (('Total' , 'Free', 'Allocated', 'Unallocated'), (total, free, allocated, unallocated))

from cliff.command import Command

class FloatingipSensu(Command):
    """sensu alert for floatingips"""

    def get_parser(self, prog_name):
        parser = super(FloatingipSensu, self).get_parser(prog_name)
        parser.add_argument('--limit', '-l', default=10,
                            help='specify the limit to trigger sensu alert (default: %(default)s; )',
                            type=int)
        return parser

    def take_action(self, parsed_args):
	error = False
	fips = self.app.cloud_obj.networks.list_floating_ips()
	down = [ip for ip in fips if ip.state =='down']
	error_msg = ''
	if len(down) > 0:
		error_msg += '{} floating ip(s) in down state'.format(len(down))
		error = True

	free_count = self.app.cloud_obj.networks.free_floating_ips
	if free_count <= parsed_args.limit:
		error_msg += '{} Free Floatingips, less than limit of {} '.format(free_count, parsed_args.limit)
		error = True

	if not error:
		return 'OK'
	
	raise Exception(error_msg)
	
