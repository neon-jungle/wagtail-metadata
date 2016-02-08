from django.db import models
from wagtail.wagtailcore.models import Site


class SitePreferences(models.Model):
    site = models.OneToOneField(Site, unique=True, db_index=True, editable=False)
    automated_scanning = models.BooleanField(default=False, help_text='Conduct automated sitewide scans for broken links, and send emails if a problem is found.')
