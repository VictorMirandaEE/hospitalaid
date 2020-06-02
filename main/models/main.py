from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Hospital(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    postal_code = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def aidrequest_supply_count(self):
        return self.aidrequest_set.filter(type="supply").count()

    def aidrequest_repair_count(self):
        return self.aidrequest_set.filter(type="repair").count()

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
        ("supply", _("New equipment/supply request")),
        ("repair", _("Existing equipment repair")),
    ]
    STATUS = [
        ("unassigned", _("Unassigned")),
        ("in_progress", _("In progress")),
        ("closed", _("Closed")),
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name=_("hospital"))
    type = models.CharField(max_length=32, choices=REQUEST_TYPE, verbose_name=_("type"))
    status = models.CharField(max_length=16, choices=STATUS, default='unassigned')
    comments = models.CharField(max_length=200, blank=True, verbose_name=_("comments"))

    title = models.CharField(max_length=50, verbose_name=_("title"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))

    manufacturer = models.CharField(max_length=16, blank=True, verbose_name=_("manufacturer"))
    model = models.CharField(max_length=16, blank=True, verbose_name=_("model"))
    serial_number = models.CharField(max_length=16, blank=True, verbose_name=_("serial number"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return "{}".format(self.title,)
