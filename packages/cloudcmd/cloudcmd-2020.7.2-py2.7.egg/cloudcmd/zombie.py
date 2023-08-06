from cliff.lister import Lister

class ZombieList(Lister):
    """List Zombie resource."""


    def take_action(self, args):
	resources = self.app.cloud_obj.resources.list_zombie_resources_by_tenants()
        return (('Resource Type', 'Resource ID', 'Tenant ID' ),((resource.resource_type, resource.id, resource.tenant_id if hasattr(resource, 'tenant_id') else 'N/A') for resource in resources))

from cliff.show import ShowOne

class ZombieStats(ShowOne):
	"""Show Zombie Resource stats"""

	def take_action(self, args):
		resources = self.app.cloud_obj.resources.list_zombie_resources_by_tenants()

		from  toolz import countby
		dic = countby(lambda x: x.resource_type, resources)

		from collections import OrderedDict
		ordered_dic  = OrderedDict(dic)

		return((key for key in ordered_dic.keys()), (ordered_dic[key] for key in ordered_dic.keys()))
