from django.contrib import admin
from .models import Post, Like, Comment

admin.site.register(Like)
admin.site.register(Comment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('test', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def test(self, object):
        return f'{object.author} - {object.text}'
