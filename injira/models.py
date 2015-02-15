from django.db import models

class Contact( models.Model):
    """
    Models for a contact
    """
    nom = models.CharField( max_length = 30 )
    mail = models.EmailField( max_length = 100 )
    staff = models.BooleanField( default = False )


