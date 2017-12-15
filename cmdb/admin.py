from django.contrib import admin
from cmdb.models import table_basic, table_content, table_head

# Register your models here.
class tableBasicAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'table_columns', 'table_rows', 'update_time')
    search_fields = ['table_name']

    fieldsets = (
        ['Main', {
            'fields': ('table_name', 'table_columns', 'table_rows'),
        }],
        ['Advance', {
            'classes': ('collapse',),
            'fields': ('update_time',),
        }],
    )

class tableContentAdmin(admin.ModelAdmin):
    list_display = ('table_id', 'cell_column', 'cell_row', 'cell_content')
    search_fields = ['table_id']

    fieldsets = (
        ['Main', {
            'fields': ('table_id', 'cell_column', 'cell_row', 'cell_content'),
        }],
        ['Advance', {
            'classes': ('collapse',),
            'fields': (),
        }],
    )

class tableHeadAdmin(admin.ModelAdmin):
    list_display = ('table_id', 'head_column', 'head_content')
    search_fields = ['table_id']

    fieldsets = (
        ['Main', {
            'fields': ('table_id', 'head_column', 'head_content'),
        }],
        ['Advance', {
            'classes': ('collapse',),
            'fields': (),
        }],
    )

admin.site.register(table_basic, tableBasicAdmin)
admin.site.register(table_content, tableContentAdmin)
admin.site.register(table_head, tableHeadAdmin)
