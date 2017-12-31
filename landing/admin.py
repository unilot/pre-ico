from django.contrib import admin

from . import models
from .admin_models import publication, roadshow, adviser


admin.site.register(models.Publication, publication.PublicationAdmin)
admin.site.register(models.Roadshow, roadshow.RoadshowAdmin)
admin.site.register(models.Adviser, adviser.AdvisorAdmin)
