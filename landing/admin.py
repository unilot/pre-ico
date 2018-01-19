from django.contrib import admin

from . import models
from .admin_models import publication, roadshow, adviser, team_member


admin.site.register(models.Publication, publication.PublicationAdmin)
admin.site.register(models.Roadshow, roadshow.RoadshowAdmin)
admin.site.register(models.Adviser, adviser.AdvisorAdmin)
admin.site.register(models.TeamMember, team_member.TeamMemberAdmin)
admin.site.register((models.Lead,))
