from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class SensorData(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_type = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField()

class Alert(models.Model):
    alert_id = models.AutoField(primary_key=True)
    alert_type = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField()
    recommendation = models.TextField()
    status = models.CharField(max_length=50)

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField()
