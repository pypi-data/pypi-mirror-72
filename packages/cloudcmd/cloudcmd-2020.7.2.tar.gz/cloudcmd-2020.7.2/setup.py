from setuptools import setup, find_packages

PROJECT = 'cloudcmd'
VERSION = '2020.07.02'

setup(name=PROJECT,
      version=VERSION,
      description='cloud command line tools',
      url='https://github.com/Hawkgirl/cloudcmd/',
      author='Hawkgirl',
      install_requires=['cliff'],
      maintainer='Hawkgril',
      maintainer_email='hawkgirlgit@gmail.com',
      license='BSD',
      packages=find_packages(),
      include_package_data=True,

      entry_points={
        'console_scripts': [
            'cloudcmd = cloudcmd.main:main'
        ],
        'cloudcmd.client': [
	    'instance-list = cloudcmd.instance:InstanceList',
	    'instance-show = cloudcmd.instance:InstanceShow',
	    'hypervisor-list = cloudcmd.hypervisor:HypervisorList',
	    'hypervisor-show = cloudcmd.hypervisor:HypervisorShow',
	    'router-list = cloudcmd.router:RouterList',
	    'volume-list = cloudcmd.volumes:VolumeList',
	    'volume-show = cloudcmd.volumes:VolumeShow',
	    'floatingip-list = cloudcmd.floatingips:FloatingipsList',
	    'floatingip-show = cloudcmd.floatingips:FloatingipShow',
	    'floatingip-summary = cloudcmd.floatingips:FloatingipSummary',
	    'tenant-list = cloudcmd.tenants:TenantList',
	    'tenant-show = cloudcmd.tenants:TenantShow',
	    'tenant-resources-list = cloudcmd.tenants:TenantResourceList',
	    'service-list = cloudcmd.services:ServicesList',
	    'token-create = cloudcmd.token:TokenCreate',
	    'zombie-list = cloudcmd.zombie:ZombieList',
	    'zombie-stats = cloudcmd.zombie:ZombieStats',
	    'sensu-services = cloudcmd.services:ServicesSensu',
	    'sensu-instances = cloudcmd.instance:InstancesSensu',
	    'sensu-hypervisor = cloudcmd.hypervisor:HypervisorSensu',
	    'sensu-volumes = cloudcmd.volumes:VolumeSensu',
	    'sensu-floatingip = cloudcmd.floatingips:FloatingipSensu',
	    'graphite-instance-metrics = cloudcmd.graphite:GraphiteInstanceMetrics',
	    'graphite-metrics = cloudcmd.graphite:GraphiteMetrics'
        ],
	},

      zip_safe=False,
      platforms=['Any'],
      )
