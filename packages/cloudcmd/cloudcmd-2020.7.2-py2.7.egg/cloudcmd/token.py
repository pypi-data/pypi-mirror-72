from cliff.show import ShowOne

class TokenCreate(ShowOne):
	"""Creates new token"""

	def take_action(self, args):
		token  = self.app.cloud_obj.identity.create_token()

		return (('Token', 'Auth-URL', 'Project-Name', 'Username', 'Issued-time', 'Expiry-time', 'Is-scoped', 'Is-Federated', 'Roles'), (token.oid, token.auth_url, token.tenant_name, token.username, token.issued_time, token.expiry_time, token.is_scoped, token.is_federated, token.roles ))
