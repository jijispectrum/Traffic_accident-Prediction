from django.db import models

class TrafficData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    traffic_volume = models.IntegerField()
    speed_limit = models.IntegerField()
    visibility = models.IntegerField()
    Weather_condition = models.CharField(max_length=100)
    lighting_condition = models.CharField(max_length=100)
    accident_severity = models.IntegerField()

    def __str__(self):
        return f"Accident {self.id} - {self.latitude}, {self.longitude}"

    class Meta:
        verbose_name = 'Traffic Data'
        verbose_name_plural = 'Traffic Data'
