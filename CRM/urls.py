from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', 'CRM.views.index', name='index'),
    url(r'^home/', 'CRM.views.home', name='homepage'),
    url(r'^subscribe/', 'CRM.views.subscribe', name='subscribepage'),
    url(r'^unsubscribe/', 'CRM.views.unsubscribe', name='unsubscribepage'),
    url(r'^adminLogin/', 'CRM.views.adminLogin', name='adminLogin'),
    url(r'^logout/', 'CRM.views.logout', name='adminLogout'),
    url(r'^adminHome/', 'CRM.views.adminHome', name='adminHome'),
    url(r'^addCategory/', 'CRM.views.addCategory', name='addCategory'),
    url(r'^removeCategory/', 'CRM.views.removeCategory', name='removeCategory'),
    url(r'^sendMail/', 'CRM.views.sendMail', name='mail'),
]
