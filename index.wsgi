import sae
from pikachu import wsgi

application = sae.create_wsgi_app(wsgi.application)