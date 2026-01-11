import graphene
from .models import Product


class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(graphene.String)
    message = graphene.String()

    def mutate(self, info):
        low_stock_items = Product.objects.filter(stock__lt=10)
        names = []
        for product in low_stock_items:
            product.stock += 10  # Simulating restocking
            product.save()
            names.append(product.name)

        return UpdateLowStockProducts(
            updated_products=names,
            message="Stock successfully updated for low-stock products."
        )


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()