from django.db import models

class ProcessedEvent(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_id

class PaymentLog(models.Model):
    order_id = models.IntegerField(db_index=True)
    event_id = models.CharField(max_length=255, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    payment_intent = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50)  
    raw = models.JSONField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
