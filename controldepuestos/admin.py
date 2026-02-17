from django.contrib import admin
from .models import Puesto, Item, FormularioPuesto, RespuestaItem


@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'activo']
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ['activo']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'orden', 'activo']
    list_filter = ['categoria', 'activo']
    list_editable = ['orden', 'activo']
    ordering = ['categoria', 'orden']


class RespuestaInline(admin.TabularInline):
    model = RespuestaItem
    extra = 0
    readonly_fields = ['item', 'estado', 'justificacion']
    can_delete = False


@admin.register(FormularioPuesto)
class FormularioPuestoAdmin(admin.ModelAdmin):
    list_display = ['puesto', 'fecha', 'codigo_oficial', 'completado', 'created_at']
    list_filter = ['puesto', 'fecha', 'completado']
    readonly_fields = ['created_at']
    inlines = [RespuestaInline]
    date_hierarchy = 'fecha'