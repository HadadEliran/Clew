from django.db import models

class MedicationPeriodEvent(models.Model):
    patient_id = models.CharField(name = "patient_id", max_length=30)
    medication_name = models.CharField(name = "medication_name", max_length=100)
    action_type = models.CharField(name = "action_type", max_length=30)
    action_activation_date = models.DateField(name = "action_activation_date")

    class Meta:
        db_table = "medication_period_events"