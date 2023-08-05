from drf_spectacular.extensions import OpenApiAuthenticationExtension


class SessionScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework.authentication.SessionAuthentication'
    name = 'cookieAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'Session',
        }


class BasicScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework.authentication.BasicAuthentication'
    name = 'basicAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'basic',
        }


class TokenScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework.authentication.TokenAuthentication'
    name = 'tokenAuth'
    match_subclasses = True

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': self.target.keyword,
        }
