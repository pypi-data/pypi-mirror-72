from cliff.lister import Lister

class HypervisorList(Lister):
    """List Hyperviors."""

    def take_action(self, args):
	hypervisors = self.app.cloud_obj.compute.list_hypervisors()
        return (('ID', 'Name', 'State', 'Status', 'Instances-Count', 'Used-memory(%)', 'Used-cpu(%)' ),
                ((h.id, h.name, h.state, h.status, h.running_vms, h.memory_used_percentage, h.vpcus_used_percentage) for h in hypervisors))

from cliff.show import ShowOne

class HypervisorShow(ShowOne):
	"""Show Hypervisor information."""
	def get_parser(self, prog_name):
        	parser = super(ShowInstance, self).get_parser(prog_name)
        	parser.add_argument('hypervisor_id', help='The hypervisor id.')
        	return parser

	def take_action(self, args):
		return (('TODO'),('TODO'))

from cliff.command import Command

class HypervisorSensu(Command):
    """sensu alert for Hypervisor"""

    def take_action(self, parsed_args):
	hypervisors = self.app.cloud_obj.compute.list_hypervisors()
	count = 0
	error = False
	msg = ''
	memory_msg = ''
	cpu_msg = ''
	for hypervisor in hypervisors:
		if hypervisor.status == 'disabled' or  hypervisor.state == 'down':
                        count += 1
			error = True
                        msg += '[Name:{} State:{} Status:{}]'.format(hypervisor.name, hypervisor.state, hypervisor.status)

		if hypervisor.vpcus_used_percentage > 70:
			cpu_msg += '[{} crossed 70% vcpu limit] '.format(hypervisor.name)
			error = True

		if hypervisor.memory_used_percentage > 70:
			memory_msg += '[{} crossed 70% memory limit] '.format(hypervisor.name)
			error = True

	
	if error == False:
		return 'OK'
	hyperisor_msg = ''
	if count > 0:
		hyperisor_msg = '{}  hypervisor(s) in down/disabled state. {}'.format(count, msg)

	full_msg = hyperisor_msg + memory_msg + cpu_msg
	raise Exception(full_msg)
	
