from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'^$', 'pqpro.views.entry'),
    (r'^panel$', 'pqpro.views.panel'),
    (r'^panel/$', 'pqpro.views.panel'),
    
)
