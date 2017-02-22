from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models.mymodel import Base, DBSession

# add these imports
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy 


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    #config = Configurator(settings=settings)
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy('somesecret'),
        authorization_policy=ACLAuthorizationPolicy(),
        default_permission='view'
    )

    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
     # update building the configurator to pass in our policies
   
    return config.make_wsgi_app()