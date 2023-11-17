from django.contrib import admin
from .models import View
from .models import Event

from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

# класс обработки данных
class ViewResource(resources.ModelResource):
    class Meta:
        model = View

# вывод данных на странице
class ViewAdmin(ImportExportModelAdmin):
    list_display = ('reg_time', 'uid', 'site_id')
    resource_classes = [ViewResource]

admin.site.register(View, ViewAdmin)

# класс обработки данных
class EventResource(resources.ModelResource):
    class Meta:
        model = Event

# вывод данных на странице
class EventAdmin(ImportExportModelAdmin):
    list_display = ('uid', 'tag')
    resource_classes = [EventResource]

admin.site.register(Event, EventAdmin)