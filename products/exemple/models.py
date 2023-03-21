from django.db import models
from django.conf import settings


class Product(models.Model):
    def __str__(self):
        if hasattr(self, "activity"):
            return f"Product: {self.activity}"
        elif hasattr(self, "package"):
            return f"Product: {self.package}"
        elif hasattr(self, "voucher"):
            return f"Product: {self.voucher}"


class ActivityManager(models.Manager):
    def create(self, *args, **kwargs):
        product = Product.objects.create()
        return super().create(*args, **kwargs, product=product)


class Activity(models.Model):
    product = models.OneToOneField("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    objects = ActivityManager()

    class Meta:
        verbose_name_plural = "activities"

    def __str__(self):
        return self.name


class PackageManager(models.Manager):
    def create(self, *args, **kwargs):
        product = Product.objects.create()
        return super().create(*args, **kwargs, product=product)


class Package(models.Model):
    product = models.OneToOneField("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    activity = models.ForeignKey(
        "Activity", on_delete=models.CASCADE, related_name="packages"
    )
    number_of_sessions = models.IntegerField(default=1)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )

    objects = PackageManager()

    @property
    def total_price(self):
        total = self.activity.unit_price * self.number_of_sessions
        return total - total * self.discount / 100

    def __str__(self):
        return f"{self.name} ({self.number_of_sessions})"


class VoucherManager(models.Manager):
    def create(self, *args, **kwargs):
        product = Product.objects.create()
        return super().create(*args, **kwargs, product=product)


class Voucher(models.Model):
    product = models.OneToOneField("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    packages = models.ManyToManyField("Package", related_name="vouchers")
    activities = models.ManyToManyField("Activity", related_name="vouchers")

    objects = VoucherManager()

    def __str__(self):
        return self.name


class OrderLine(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="orders"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="order_lines",
    )
    number = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name_plural = "order lines"
