from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def soft_delete(self):
        self.delete_date = timezone.now()
        self.save()


class Partner(BaseModel):
    name = models.CharField(null=False, max_length=255)
    mcc = models.CharField(null=False, max_length=4)

    class Meta:
        db_table = "partner"


class Bank(BaseModel):
    name = models.CharField(null=False, max_length=255)
    partner = models.ManyToManyField(Partner)

    class Meta:
        db_table = "bank"


class Card(BaseModel):
    name = models.CharField(null=False, max_length=255)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    class Meta:
        db_table = "card"


class User(AbstractUser):
    phone_number = models.CharField(max_length=255, null=False)
    card = models.ManyToManyField(
        Card, through="UserCard", through_fields=("user", "card")
    )

    class Meta:
        db_table = "user"


class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_card"


class ProductType(BaseModel):
    name = models.CharField(null=False, max_length=255)
    mcc = models.CharField(null=False, max_length=4)

    class Meta:
        db_table = "product_type"


class PartnerCashback(BaseModel):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    cashback = models.IntegerField(null=True)

    class Meta:
        db_table = "partner_cashback"


class CardCashback(BaseModel):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    cashback = models.IntegerField(null=False)

    class Meta:
        db_table = "card_cashback"


class UserCashback(BaseModel):
    user_card = models.ForeignKey(UserCard, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    cashback = models.IntegerField()

    class Meta:
        db_table = "user_cashback"
