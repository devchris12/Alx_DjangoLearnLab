from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Author, Book, Library, Librarian, UserProfile

# Register basic models
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)

# UserProfile admin configuration
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'date_created', 'date_modified')
    list_filter = ('role', 'date_created')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('date_created', 'date_modified')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',)
        }),
    )

# Inline UserProfile in User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ('role',)

# Extend the existing User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
