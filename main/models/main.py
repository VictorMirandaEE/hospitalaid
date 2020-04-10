from django.contrib.auth import get_user_model
from django.db import models


class Hospital(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    postal_code = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.city, self.country)


class AidRequest(models.Model):
    REQUEST_TYPE = [
        ("equipment_repair", "Existing equipment repair"),
        ("equipment_request", "New equipment request"),
        ("supply_request", "New supply request"),
        ("other_request", "Other request"),
    ]
    STATUS_TYPE = [
        ("inprogress", "In progress"),
        ("completed", "Completed"),
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=REQUEST_TYPE)
    details = models.TextField(max_length=2000)

    equipment_type = models.CharField(
        max_length=50, help_text="only for new equipment request", blank=True
    )
    equipment_quantity = models.CharField(
        max_length=16, help_text="only for new equipment request", blank=True
    )

    supply_type = models.CharField(
        max_length=50, help_text="only for new supply request", blank=True
    )
    supply_quantity = models.CharField(
        max_length=16, help_text="only for new supply quantity", blank=True
    )

    equipment_brand = models.CharField(
        max_length=16, help_text="only for equipment repair", blank=True
    )
    equipment_model = models.CharField(
        max_length=16, help_text="only for equipment repair", blank=True
    )
    equipment_serialno = models.CharField(
        max_length=16, help_text="only for equipment repair", blank=True
    )

    assigned_to = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, blank=True, null=True
    )
    status = models.CharField(max_length=16, choices=STATUS_TYPE, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def friendly_status(self):
        if self.assigned_to:
            return self.get_status_display()
        else:
            return "Unassigned"

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return "{}".format(self.details,)
