# Register your models here.
from django.contrib import admin

from .forms import EditProfileForm, UserRegisterForm
from .models import *


class UserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form = EditProfileForm
        else:
            self.form = UserRegisterForm
        return super(UserAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(PicturestUser, UserAdmin)
admin.site.register(Board)
admin.site.register(Pin)
admin.site.register(Friendship)
admin.site.register(InterestsSimple)
admin.site.register(Notification)
