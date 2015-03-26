from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode

from service_discovery import service_discovery

# Fill the choice of services
sd=service_discovery()
services=sd.services()
SERVICES_ACTION_CHOICE=[]
for service in services:
    for action in services[service]:
        SERVICES_ACTION_CHOICE.append(('%s:%s' % (service,action),'%s:%s' % (service,action)))

# Fill the choice of enviroments
ENVIROMENTS_CHOICE=(
    ("dev",_("Development")),
    ("test",_("Test")),
    ("real",_("Real")),
    )
# Fill the choice of algorithms
ALGORITHMS_CHOICE=(
    ("M",_("MD5")),
    ("S",_("SHA1")),
    )

class Key(models.Model):
    '''
    User key
    '''
    
    user = models.ForeignKey(User, unique=True, null=False, blank=False, related_name='security')
    algorithm = models.CharField(_("Algorithm"), max_length=1, choices=ALGORITHMS_CHOICE, null=False, blank=False)
    key = models.CharField(_("Key"), max_length=50, null=False, blank=False)
    
    def clean(self):
        if len(self.key)!=32:
            from django.core.exceptions import ValidationError
            raise ValidationError(_('Key has to be 32 bytes length'))
        
    def public_key(self):
        return "$%s$%s" % (self.user.username,self.algorithm,self.key)
    
    def __unicode__(self):
        return smart_unicode(self.user.username);


class Profile(models.Model):
    '''
    Security profile
    '''
    
    user = models.ForeignKey(User, null=False, blank=False, related_name='profile')
    enviroment = models.CharField(_("Enviroment"), max_length=10, choices=ENVIROMENTS_CHOICE, null=False, blank=False)
    permissions = models.CharField(_("Service/Action"), max_length=50, choices=SERVICES_ACTION_CHOICE, null=False, blank=False)
    
    class Meta:
        unique_together = ('user','permissions')
    
    def __unicode__(self):
        return smart_unicode("%s: %s" % (self.user.username,self.permissions.replace(":","->")))
