from import_export import resources
from .models import Contacto


class ContactoResource(resources.ModelResource):

   class Meta:
    model = Contacto
