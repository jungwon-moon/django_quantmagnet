from django.contrib import admin
from api.models import Holiday
# Register your models here.


class ModelAdmin(admin.ModelAdmin):
    using = 'gcp'
    search_fields = ['calnd_dd']
    list_display = ['calnd_dd', 'kr_dy_tp', 'holdy_nm']

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


admin.site.register(Holiday, ModelAdmin)
