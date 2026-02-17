from django.db import models
from django.utils.text import slugify


class Puesto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Puesto'
        verbose_name_plural = 'Puestos'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Item(models.Model):
    PUESTO = 'puesto'
    OFICIAL = 'oficial'
    CATEGORIA_CHOICES = [
        (PUESTO, 'Puesto'),
        (OFICIAL, 'Oficial'),
    ]

    nombre = models.CharField(max_length=120)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES)
    orden = models.PositiveSmallIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['categoria', 'orden', 'nombre']
        verbose_name = 'Ítem'
        verbose_name_plural = 'Ítems'

    def __str__(self):
        return f'[{self.get_categoria_display()}] {self.nombre}'


class FormularioPuesto(models.Model):
    puesto = models.ForeignKey(Puesto, on_delete=models.PROTECT, related_name='formularios')
    fecha = models.DateField()
    codigo_oficial = models.CharField(max_length=60, verbose_name='Código del Oficial')
    completado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['puesto', 'fecha']
        ordering = ['-fecha', 'puesto__nombre']
        verbose_name = 'Formulario'
        verbose_name_plural = 'Formularios'

    def __str__(self):
        return f'{self.puesto.nombre} — {self.fecha} — {self.codigo_oficial}'


class RespuestaItem(models.Model):
    BUENO = 'B'
    MALO = 'M'
    NO_HAY = 'N'
    ESTADO_CHOICES = [
        (BUENO, 'Bueno'),
        (MALO, 'Malo'),
        (NO_HAY, 'No hay'),
    ]

    formulario = models.ForeignKey(FormularioPuesto, on_delete=models.CASCADE, related_name='respuestas')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    justificacion = models.TextField(verbose_name='Justificación')

    class Meta:
        unique_together = ['formulario', 'item']
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        return f'{self.item.nombre}: {self.get_estado_display()}'