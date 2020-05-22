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


class ImportedHospital(models.Model):
    name = models.CharField(max_length=512)
    addr_postcode = models.CharField(max_length=32)
    addr_housenumber = models.CharField(max_length=32)
    addr_street = models.CharField(max_length=64)
    addr_city = models.CharField(max_length=64)
    # based on https://stackoverflow.com/a/30711177/375670
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # TODO: Figure out how to determine country (might have to be derived from coords)

    def __str__(self):
        return "{} ({})".format(self.name, self.addr_city)


class AidRequest(models.Model):
    REQUEST_TYPE = [
        ("supply", "New equipment/supply request"),
        ("repair", "Existing equipment repair"),
    ]
    STATUS = [
        ("unassigned", "Unassigned"),
        ("in_progress", "In progress"),
        ("closed", "Closed"),
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=REQUEST_TYPE)
    status = models.CharField(max_length=16, choices=STATUS, default='unassigned')
    comments = models.CharField(max_length=200, blank=True)

    title = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)

    manufacturer = models.CharField(max_length=16, blank=True)
    model = models.CharField(max_length=16, blank=True)
    serial_number = models.CharField(max_length=16, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return "{}".format(self.comments,)
