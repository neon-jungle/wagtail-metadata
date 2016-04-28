from __future__ import unicode_literals

from django.conf.urls import include, url
from django.core import urlresolvers
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^metadata/', include(urls)),
    ]


@hooks.register('register_settings_menu_item')
def register_menu_settings():
    return MenuItem(
        'Metadata',
        urlresolvers.reverse('wagtailmetadata'),
        classnames='icon icon-pick',
        order=300
    )
