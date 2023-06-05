from django.contrib import admin

from post_service.models import (
    Post,
    Commentary,
    UserProfile,
)


admin.site.register(Post)
admin.site.register(Commentary)
admin.site.register(UserProfile)
