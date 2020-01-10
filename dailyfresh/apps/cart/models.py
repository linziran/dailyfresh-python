from django.db import models

# Create your models here.
class Car(models.Model):
    id = models.AutoField(primary_key=True)
    count = models.IntegerField(verbose_name="商品数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    goodid = models.ForeignKey(to='goods.GoodsSKU',to_field='id',on_delete=models.CASCADE,verbose_name='商品id')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name