from controldepuestos.models import Item

Item.objects.all().delete()

ITEMS_PUESTO = [
    'Toma corrientes',
    'Refrigerador',
    'Cafetera (Coffeemaker)',
    'Microondas',
    'Puerta(s)',
    'Ventanas',
    'Celular del puesto',
    'Pilas / Baterías',
    'Fluorescentes / Tubos',
    'Llave(s) de tubería',
    'Luces / Bombillos',
    'Monitor(es) de seguridad',
    'Cámara(s) de seguridad',
    'Teclado',
    'Mouse',
    'Router / Internet',
    'Cargadores',
    'Linterna',
    'Silla',
    'Foco de emergencia',
    'Botas de hule',
    'Paraguas',
    'Servicio sanitario',
    'Escritorio / Mesa de trabajo',
    'Extintor',
    'Botiquín de primeros auxilios',
]

ITEMS_OFICIAL = [
    'Zapatos negros',
    'Pantalón de vestir negro',
    'Camisa de la empresa',
    'Gafete de identificación',
    'Cinturón negro',
]

for i, nombre in enumerate(ITEMS_PUESTO, 1):
    Item.objects.create(nombre=nombre, categoria='puesto', orden=i)

for i, nombre in enumerate(ITEMS_OFICIAL, 1):
    Item.objects.create(nombre=nombre, categoria='oficial', orden=i)

print(f"Items creados: {Item.objects.count()}")
print("Puesto:", Item.objects.filter(categoria='puesto').count())
print("Oficial:", Item.objects.filter(categoria='oficial').count())