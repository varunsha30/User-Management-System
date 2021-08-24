from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin

admin.site.site_header = 'Login'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Site Admin'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    change_user_password_template = 'templates/registration/password_reset_form.html'
    readonly_fields = [
        'date_joined',
        'last_login',
    ]

    actions = [
        'activate_users',
        'deactivate_users',
    ]

    # makes staff see only their detail

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_superuser else qs.filter(is_superuser=False, is_staff=False) | qs.filter(id=user.id)

    def activate_users(self, request, queryset):
        assert request.user.has_perm('auth.change_user')
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, 'Activated {} users.'.format(cnt))

    activate_users.short_description = 'Activate Users'  # type: ignore

    def deactivate_users(self, request, queryset):
        assert request.user.has_perm('auth.change_user')
        cnt = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(request, 'Deactivated {} users.'.format(cnt))

    deactivate_users.short_description = 'Deactivate Users'  # type: ignore

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('auth.change_user'):
            del actions['activate_users', 'deactivate_users']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_staff',
                'is_superuser',
                'user_permissions',
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
