# Register your models here.
from django.contrib import admin
from custom_user.models import PicturestUser
from .forms import EditProfileForm, UserRegisterForm


class UserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form = EditProfileForm
        else:
            self.form = UserRegisterForm
        return super(UserAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(PicturestUser, UserAdmin)
