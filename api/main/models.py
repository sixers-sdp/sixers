from django.db import models


ORDER_STATE_NEW = 'new'
ORDER_STATE_DELIVERY = 'delivery'
ORDER_STATE_FINISHED = 'finished'
ORDER_STATE_ABORTED = 'aborted'

ORDER_STATE_CHOICES = [
    (s, s)
    for s in [ORDER_STATE_NEW, ORDER_STATE_DELIVERY, ORDER_STATE_FINISHED, ORDER_STATE_ABORTED]
]


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    table_number = models.IntegerField()

    products = models.ManyToManyField(Product)
    state = models.CharField(
        default=ORDER_STATE_NEW,
        choices=ORDER_STATE_CHOICES,
        max_length=24
    )

    def __str__(self):
        return f"{self.state}: {self.updated_at}"
