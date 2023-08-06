from cliff.lister import Lister

class VolumeList(Lister):
    """List Volumes."""

    def take_action(self, args):
	volumes = self.app.cloud_obj.volumes.list_volumes()
        return (('ID', 'Name', 'Size', 'Status' ),
                ((v.id, v.name, v.size, v.status) for v in volumes))

from cliff.show import ShowOne

class VolumeShow(ShowOne):
	"""Show volume information."""
	def get_parser(self, prog_name):
        	parser = super(ShowInstance, self).get_parser(prog_name)
        	parser.add_argument('volume_id', help='The volume id.')
        	return parser

	def take_action(self, args):
		return (('TODO'),('TODO'))

from cliff.command import Command

class VolumeSensu(Command):
    """sensu alert for volume"""

    def take_action(self, parsed_args):
	volumes = self.app.cloud_obj.volumes.get_volumes_by_error_state()
	if len(volumes) == 0:
		return 'OK'

	msg = ''
	for volume in volumes:
		msg += '[Id:{} Name:{} ] '.format(volume.id, volume.name)

	raise Exception('{} volume(s) in Error state. {}'.format(len(volumes), msg))
	
