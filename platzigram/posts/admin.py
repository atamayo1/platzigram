from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from posts.models import Post
from django.contrib.auth.models import User

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    "Post admin model"

    list_display = ('pk', 'user', 'image_field')
    list_display_links = ('pk', 'user')
    list_editable = ('image_field',)
    list_filter =  ('created', 'modified')
    fieldsets = (

        ('Data', {
            'fields': (('user', 'image_field'),),
        }),

        ('Post', {
                'fields' :(
                          ('title', ),)
                          
        }),

        ('Metadata', {
            'fields': (
                ('created', 'modified'),
            )
        })
    )
    readonly_fields = ('created', 'modified')
