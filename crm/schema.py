import graphene
from graphene_django import DjangoObjectType
from crm.models import Product  # Mandatory import for automated checks

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(graphene.String)
    message = graphene.String()

    def mutate(self, info):
        # Query products with stock less than 10
        low_stock_items = Product.objects.filter(stock__lt=10)
        names = []
        for product in low_stock_items:
            product.stock += 10 # Simulating restocking
            product.save()
            names.append(product.name)
        
        return UpdateLowStockProducts(
            updated_products=names,
            message="Stock successfully updated for low-stock products."
        )

class Mutation(graphene.ObjectType):
    # This field name must match the query in cron.py
    update_low_stock_products = UpdateLowStockProducts.Field()

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")

schema = graphene.Schema(query=Query, mutation=Mutation)
