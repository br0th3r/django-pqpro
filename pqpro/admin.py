from django.contrib import admin
from pqpro.models import Profile,Key

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'enviroment', 'permissions')
    # Will add a filtering column on the right to make easy to look for registers
    list_filter = ['permissions']
    # Will add a search box for questions on the top
    search_fields = ['user__username','permissions']
admin.site.register(Profile, ProfileAdmin)

class KeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'algorithm', 'key')
    # Will add a filtering column on the right to make easy to look for registers
    list_filter = ['algorithm']
    # Will add a search box for questions on the top
    search_fields = ['user__username']
admin.site.register(Key,KeyAdmin)

