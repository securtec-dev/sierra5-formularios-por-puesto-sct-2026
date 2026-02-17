from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Puesto, Item, FormularioPuesto, RespuestaItem


def dashboard(request):
    hoy = timezone.localdate()
    puestos = Puesto.objects.filter(activo=True)
    completados = set(
        FormularioPuesto.objects
        .filter(fecha=hoy, completado=True)
        .values_list('puesto_id', flat=True)
    )
    data = [{'puesto': p, 'completado': p.id in completados} for p in puestos]
    total = puestos.count()
    hechos = len(completados)
    return render(request, 'dashboard.html', {
        'data': data,
        'hoy': hoy,
        'total': total,
        'hechos': hechos,
        'pendientes': total - hechos,
    })


def formulario(request, slug):
    puesto = get_object_or_404(Puesto, slug=slug, activo=True)
    hoy = timezone.localdate()

    if FormularioPuesto.objects.filter(puesto=puesto, fecha=hoy, completado=True).exists():
        messages.warning(request, f'El puesto "{puesto.nombre}" ya fue completado hoy.')
        return redirect('dashboard')

    items_puesto = list(Item.objects.filter(categoria=Item.PUESTO, activo=True).order_by('orden', 'nombre'))
    items_oficial = list(Item.objects.filter(categoria=Item.OFICIAL, activo=True).order_by('orden', 'nombre'))
    all_items = items_puesto + items_oficial

    errores = []
    post_data = {}

    if request.method == 'POST':
        post_data = request.POST
        codigo = request.POST.get('codigo_oficial', '').strip()

        if not codigo:
            errores.append('El código del oficial es requerido.')

        respuestas = []
        for item in all_items:
            estado = request.POST.get(f'estado_{item.id}', '').strip()
            justificacion = request.POST.get(f'justificacion_{item.id}', '').strip()

            if not estado:
                errores.append(f'Falta estado: {item.nombre}')
            if not justificacion:
                errores.append(f'Falta justificación: {item.nombre}')

            respuestas.append({'item': item, 'estado': estado, 'justificacion': justificacion})

        if not errores:
            form_obj = FormularioPuesto.objects.create(
                puesto=puesto,
                fecha=hoy,
                codigo_oficial=codigo,
                completado=True,
            )
            RespuestaItem.objects.bulk_create([
                RespuestaItem(
                    formulario=form_obj,
                    item=r['item'],
                    estado=r['estado'],
                    justificacion=r['justificacion'],
                ) for r in respuestas
            ])
            messages.success(request, f'✓ {puesto.nombre} — Formulario guardado.')
            return redirect('dashboard')

    return render(request, 'formulario.html', {
        'puesto': puesto,
        'items_puesto': items_puesto,
        'items_oficial': items_oficial,
        'errores': errores,
        'post_data': post_data,
        'hoy': hoy,
    })