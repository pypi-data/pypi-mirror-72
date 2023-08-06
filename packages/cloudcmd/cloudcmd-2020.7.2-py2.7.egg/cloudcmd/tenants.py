from cliff.lister import Lister

class TenantList(Lister):
    """List tenants."""

    def take_action(self, args):
	tenants = self.app.cloud_obj.identity.list_tenants()
        return (('ID', 'Name', 'Status'),
                ((t.id, t.name, t.status) for t in tenants))

from cliff.show import ShowOne

class TenantShow(ShowOne):
	"""Show tenant information."""
	def get_parser(self, prog_name):
        	parser = super(TenantShow, self).get_parser(prog_name)
        	parser.add_argument('tenant_id', help='The tenant id.')
        	return parser

	def take_action(self, args):
		tenant = self.app.cloud_obj.identity.get_tenant_by_id(args.tenant_id)

		return (('ID', 'Name', 'Status' ), (tenant.id, tenant.name, tenant.status))

class TenantResourceList(Lister):
    """List tenants resources"""

    def take_action(self, args):
	resources = []
	# resource group is dict of dicts. 
	import collections
	resource_group =  collections.defaultdict(int)
	for resource in self.app.cloud_obj.resources.list_all_resources():
            if not hasattr(resource, 'tenant_id'):
			continue
	    if resource.tenant_id not in resource_group:
			resource_group[resource.tenant_id] = collections.defaultdict(int)
	    if resource.resource_type not in resource_group[resource.tenant_id]:
			resource_group[resource.tenant_id][resource.resource_type] = 1
	    else:
			resource_group[resource.tenant_id][resource.resource_type] += 1

	tenant_names = collections.defaultdict(lambda :  'N/A')
	tenants = self.app.cloud_obj.identity.list_tenants_cache()
	for key in tenants:
		tenant_names[key] = tenants[key]['name']

        return (('Tenant ID', 'Tenant Name', 'instances', 'SecGroups', 'Networks', 'Subnets', 'Ports', 'FloatingIps', 'Volumes', 'SnapShots'), ((key, tenant_names[key], resource_group[key]['instance'], resource_group[key]['securitygroup'], resource_group[key]['network'], resource_group[key]['subnet'],resource_group[key]['port'],resource_group[key]['floatingip'], resource_group[key]['volume'], resource_group[key]['snapshot']) for key in resource_group))
