from __future__ import division

from cliff.lister import Lister
import datetime
import time

class GraphiteMetrics(Lister):
    """List cloud metrics in Graphite format"""

    @property
    def formatter_default(self):
        return 'value'

    def take_action(self, args):
	metrics = self.app.cloud_obj.resources.list_metrics()
        return (('', '', '' ), ((metric.name, metric.value, metric.timestamp) for metric in metrics))

class GraphiteInstanceMetrics(Lister):
    """List Instance usage metrics in Graphite format"""

    @property
    def formatter_default(self):
        return 'value'

    def get_parser(self, prog_name):
        parser = super(GraphiteInstanceMetrics, self).get_parser(prog_name)
        parser.add_argument('--last_n_hours', '-n', default=6,
                            help='specify the metrics to be collected '
                                 'for last n hours (default: %(default)s; '
                                 'maximum: 100)', type=int)
        parser.add_argument('--sample', '-s', default=12,
                            help='specify the no of samples to collected'
                                 'for last n hours (default: %(default)s; '
                                 'maximum: 100)', type=int)
        return parser

    def take_action(self, args):
	count = args.sample
	hours = args.last_n_hours
	instances = self.app.cloud_obj.compute.list_instances()
	lst = []
	end = datetime.datetime.now()
	start= end - datetime.timedelta(hours=hours)

	for i in instances:
		tenant_name = 'NA'
		if i.tenant_name:
			tenant_name = i.tenant_name.replace('.', '_').replace('@', '_')
		metric_base_name = 'openstack.tenant.'+i.tenant_id+'.'+str(tenant_name)+'.instance.'+i.id+'.'+str(i.name)
		cpu_usage = i.cpu_usage(start_time = start, end_time = end, count=count)
		for u in cpu_usage:
			timestamp = datetime.datetime.strptime(u['end_time'], "%Y-%m-%dT%H:%M:%S")
			value = u['avg']
			delta = timestamp - datetime.datetime.utcfromtimestamp(0)
			metric_name = metric_base_name + '.cpu'
			t = (metric_name,value,int(delta.total_seconds()))
			lst.append(t)

		# memory stats
		mem_usage = i.mem_usage(start_time=start, end_time=end, count=count)
		for u in mem_usage:
			timestamp = datetime.datetime.strptime(u['end_time'], "%Y-%m-%dT%H:%M:%S")
			value = u['percentage']
			delta = timestamp - datetime.datetime.utcfromtimestamp(0)
			metric_name = metric_base_name + '.mem_percentage'
			t = (metric_name,value,int(delta.total_seconds()))
			lst.append(t)

		# net_tx stats
		net_tx_usage = i.net_tx_usage(start_time=start, end_time=end, count=count)
		for u in net_tx_usage:
			timestamp = datetime.datetime.strptime(u['time'], "%Y-%m-%dT%H:%M:%S")
			value = u['bytes']
			delta = timestamp - datetime.datetime.utcfromtimestamp(0)
			metric_name = metric_base_name + '.network.tx_bytes'
			t = (metric_name,value,int(delta.total_seconds()))
			lst.append(t)
		# net_rx_stats
		net_rx_usage = i.net_rx_usage(start_time=start, end_time=end, count=count)
		for u in net_rx_usage:
			timestamp = datetime.datetime.strptime(u['time'], "%Y-%m-%dT%H:%M:%S")
			value = u['bytes']
			delta = timestamp - datetime.datetime.utcfromtimestamp(0)
			metric_name = metric_base_name + '.network.rx_bytes'
			t = (metric_name,value,int(delta.total_seconds()))
			lst.append(t)

	return (('','',''), tuple(lst))

