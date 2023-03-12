from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

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
    readonly_fields = ('small_image_tmb',)


class GalleryInline(admin.TabularInline):
    model = catalog.models.ImageGallery
    readonly_fields = ('small_image_tmb',)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.creation_date.field.name,
        catalog.models.Item.change_date.field.name,
    )
    inlines = [
        MainImageInline,
        GalleryInline,
    ]
    form = ItemAdminForm
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
