import sys
import os
from os import environ
from cliff.app import App
from cliff.commandmanager import CommandManager
from cloudcmd import version
from ext_cloud import get_ext_cloud

import warnings
warnings.filterwarnings("ignore")

import logging
logging.getLogger("requests").setLevel(logging.WARNING)

class CloudcmdApp(App):

    def __init__(self, **kwargs):
        super(CloudcmdApp, self).__init__(description='cloudcmd', version=version.__version__,
                                          command_manager=CommandManager('cloudcmd.client'), **kwargs)

    def build_option_parser(self, description, version, argparse_kwargs=None):
        '''
        Introduces global arguments for the application.
        This is inherited from the framework.
        '''
        parser = super(CloudcmdApp, self).build_option_parser(
            description, version, argparse_kwargs)
        parser.add_argument('--os-identity-api-version',
                            metavar='<identity-api-version>',
                            default=environ.get('OS_IDENTITY_API_VERSION'),
                            help='Specify Identity API version to use. '
                            'Defaults to env[OS_IDENTITY_API_VERSION]'
                            ' or 3.0.')
        parser.add_argument('--os-auth-url', '-A',
                            metavar='<auth-url>',
                            default=environ.get('OS_AUTH_URL'),
                            help='Defaults to env[OS_AUTH_URL].')
        parser.add_argument('--os-username', '-U',
                            metavar='<auth-user-name>',
                            default=environ.get('OS_USERNAME'),
                            help='Defaults to env[OS_USERNAME].')
        parser.add_argument('--os-user-id',
                            metavar='<auth-user-id>',
                            default=environ.get('OS_USER_ID'),
                            help='Defaults to env[OS_USER_ID].')
        parser.add_argument('--os-password', '-P',
                            metavar='<auth-password>',
                            default=environ.get('OS_PASSWORD'),
                            help='Defaults to env[OS_PASSWORD].')
        parser.add_argument('--os-user-domain-id',
                            metavar='<auth-user-domain-id>',
                            default=environ.get('OS_USER_DOMAIN_ID'),
                            help='Defaults to env[OS_USER_DOMAIN_ID].')
        parser.add_argument('--os-user-domain-name',
                            metavar='<auth-user-domain-name>',
                            default=environ.get('OS_USER_DOMAIN_NAME'),
                            help='Defaults to env[OS_USER_DOMAIN_NAME].')
        parser.add_argument('--os-tenant-name', '-T',
                            metavar='<auth-tenant-name>',
                            default=environ.get('OS_TENANT_NAME'),
                            help='Defaults to env[OS_TENANT_NAME].')
        parser.add_argument('--os-tenant-id', '-I',
                            metavar='<tenant-id>',
                            default=environ.get('OS_TENANT_ID'),
                            help='Defaults to env[OS_TENANT_ID].')
        parser.add_argument('--os-project-id',
                            metavar='<auth-project-id>',
                            default=environ.get('OS_PROJECT__ID'),
                            help='Another way to specify tenant ID. '
                                 'This option is mutually exclusive with '
                                 ' --os-tenant-id. '
                            'Defaults to env[OS_PROJECT_ID].')
        parser.add_argument('--os-project-name',
                            metavar='<auth-project-name>',
                            default=environ.get('OS_PROJECT_NAME'),
                            help='Another way to specify tenant name. '
                                 'This option is mutually exclusive with '
                                 ' --os-tenant-name. '
                                 'Defaults to env[OS_PROJECT_NAME].')
        parser.add_argument('--os-project-domain-id',
                            metavar='<auth-project-domain-id>',
                            default=environ.get('OS_PROJECT_DOMAIN_ID'),
                            help='Defaults to env[OS_PROJECT_DOMAIN_ID].')
        parser.add_argument('--os-project-domain-name',
                            metavar='<auth-project-domain-name>',
                            default=environ.get('OS_PROJECT_DOMAIN_NAME'),
                            help='Defaults to env[OS_PROJECT_DOMAIN_NAME].')
        parser.add_argument('--os-cacert',
                            metavar='<ca-certificate>',
                            default=environ.get('OS_CACERT'),
                            help='Specify a CA bundle file to use in verifying a'
                                'TLS (https) server certificate. Defaults to'
                                'env[OS_CACERT].')
        parser.add_argument('--os-auth-token',
                            metavar='<auth-token>',
                            default=environ.get('OS_AUTH_TOKEN'),
                            help='Defaults to env[OS_AUTH_TOKEN].')
        return parser

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')
        args = self.options
        if args.os_auth_token:
            if not args.os_auth_url:
                raise Exception('ERROR: please specify --os-auth-url')
        elif all([args.os_auth_url, args.os_user_id or args.os_username,
                  args.os_password, args.os_tenant_name or args.os_tenant_id or
                  args.os_project_name or args.os_project_id]):
            kwargs = dict()
            kwargs['auth_url'] = args.os_auth_url
            kwargs['password'] = args.os_password
            if args.os_user_id:
                kwargs['user_id'] = args.os_user_id
            if args.os_username:
                kwargs['username'] = args.os_username
            if args.os_tenant_id:
                kwargs['tenant_id'] = args.os_tenant_id
            if args.os_tenant_name:
                kwargs['tenant_name'] = args.os_tenant_name
            if args.os_cacert:
                kwargs['cacert'] = args.os_cacert

            self.cloud_obj = get_ext_cloud('openstack', **kwargs)
	elif os.path.isfile('/etc/ext_cloud/ext_cloud.conf'):
	    # load from config file
            self.cloud_obj = get_ext_cloud('openstack')
        else:
            self.stderr.write(self.parser.format_usage())
            raise Exception('ERROR: please specify authentication credentials')


    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = CloudcmdApp()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
