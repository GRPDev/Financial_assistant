from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    status_alias = {
        "Success": "success",
        "Failure": "failure"
    }
    type_alias = {
        "Deposit": "deposit",
        "Withdraw": "withdraw"
    }
    status = models.CharField(max_length=10, choices=status_alias)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    type = models.CharField(max_length=10, choices=type_alias)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount} - {self.status}"