from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.gis import forms

import catalog.models

admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.Category)
admin.site.register(catalog.models.MainImage)
admin.site.register(catalog.models.ImageGallery)


class ItemAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = catalog.models.Item
        fields = '__all__'


class MainImageInline(admin.TabularInline):
    model = catalog.models.MainImage
    readonly_fields = ('image_tmb',)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    inlines = [
        MainImageInline,
    ]
    form = ItemAdminForm
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
