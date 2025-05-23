from django.contrib import admin
from .models import Machine, MachineOperator, MachineOperatorAssignment, MachineSpecification, MachineReading

class MachineReadingInline(admin.TabularInline):
    model = MachineReading
    extra = 1

class MachineSpecificationInline(admin.StackedInline):
    model = MachineSpecification
    can_delete = False

class MachineAdmin(admin.ModelAdmin):
    list_display = ('machine_number', 'manufacturer', 'model', 'installation_date', 'last_maintenance')
    search_fields = ('machine_number', 'manufacturer', 'model')
    list_filter = ('manufacturer', 'installation_date')
    inlines = [MachineSpecificationInline, MachineReadingInline]

class MachineOperatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'qualification')
    search_fields = ('name', 'employee_id')

class MachineOperatorAssignmentAdmin(admin.ModelAdmin):
    list_display = ('machine', 'operator', 'assignment_date', 'is_current')
    list_filter = ('is_current', 'assignment_date')
    search_fields = ('machine__machine_number', 'operator__name')

class MachineSpecificationAdmin(admin.ModelAdmin):
    list_display = ('machine', 'max_vibration', 'max_power', 'max_temperature')
    search_fields = ('machine__machine_number',)

class MachineReadingAdmin(admin.ModelAdmin):
    list_display = ('reading_number', 'machine', 'timestamp', 'vibration_frequency', 'power_consumption', 'temperature')
    list_filter = ('machine', 'timestamp')
    search_fields = ('machine__machine_number', 'notes')

admin.site.register(Machine, MachineAdmin)
admin.site.register(MachineOperator, MachineOperatorAdmin)
admin.site.register(MachineOperatorAssignment, MachineOperatorAssignmentAdmin)
admin.site.register(MachineSpecification, MachineSpecificationAdmin)
admin.site.register(MachineReading, MachineReadingAdmin)