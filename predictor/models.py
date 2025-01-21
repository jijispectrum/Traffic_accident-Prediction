from django.db import models

class AccidentRecord(models.Model):
    # Fields for the accident record
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField(max_length=255)
    weather_condition = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.IntegerField()  # Predicted severity level
    datetime = models.DateTimeField(auto_now_add=True)  # Timestamp of the record

    def __str__(self):
        return f"Accident at {self.location} with severity {self.severity}"
