from django.contrib import admin
from knut_server.tests.models import User, Test, Category, TestUser, Result

class UserAdmin(admin.ModelAdmin):
    pass

class TestAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class TestUserAdmin(admin.ModelAdmin):
    pass

class ResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(TestUser, TestUserAdmin)
admin.site.register(Result, ResultAdmin)