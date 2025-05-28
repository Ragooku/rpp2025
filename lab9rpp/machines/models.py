from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Machine(models.Model):
    machine_number = models.CharField(max_length=50, unique=True, verbose_name="Номер светофора")
    manufacturer = models.CharField(max_length=100, verbose_name="Производитель")
    model = models.CharField(max_length=100, verbose_name="Модель")
    installation_date = models.DateField(verbose_name="Дата установки")
    last_maintenance = models.DateField(verbose_name="Дата последнего ТО", null=True, blank=True)

    class Meta:
        verbose_name = "Светофор"
        verbose_name_plural = "Светофоры"

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.machine_number})"


class MachineOperator(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя оператора")
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="Табельный номер")
    qualification = models.CharField(max_length=100, verbose_name="Квалификация")

    class Meta:
        verbose_name = "Оператор светофора"
        verbose_name_plural = "Операторы светофоров"

    def __str__(self):
        return f"{self.name} ({self.employee_id})"


class MachineOperatorAssignment(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name="Светофор")
    operator = models.ForeignKey(MachineOperator, on_delete=models.CASCADE, verbose_name="Оператор")
    assignment_date = models.DateField(verbose_name="Дата назначения")
    is_current = models.BooleanField(default=True, verbose_name="Текущее назначение")

    class Meta:
        verbose_name = "Назначение оператора"
        verbose_name_plural = "Назначения операторов"
        unique_together = ('machine', 'operator', 'assignment_date')

    def __str__(self):
        return f"{self.operator} → {self.machine} ({self.assignment_date})"


class MachineSpecification(models.Model):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE, primary_key=True, verbose_name="Светофор")
    max_vibration = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Макс. вибрация")
    max_power = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Макс. мощность")
    max_temperature = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Макс. температура")
    recommended_power = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Реком. мощность")

    class Meta:
        verbose_name = "Технические характеристики светофора"
        verbose_name_plural = "Технические характеристики светофоров"

    def __str__(self):
        return f"Характеристики {self.machine}"


class MachineReading(models.Model):
    reading_number = models.AutoField(primary_key=True, verbose_name="№ показания")
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name="Светофор")
    timestamp = models.DateTimeField(verbose_name="Дата и время")
    vibration_frequency = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Проехало")
    power_consumption = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Стоят")
    temperature = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Температура")
    notes = models.TextField(blank=True, verbose_name="Примечания")

    class Meta:
        verbose_name = "Показание светофора"
        verbose_name_plural = "Показания светофоров"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Показание #{self.reading_number} для {self.machine} ({self.timestamp})"