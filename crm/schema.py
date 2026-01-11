import graphene
from graphene_django import DjangoObjectType
from crm.models import Product, Order, Customer
from django.db.models import Sum

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(graphene.String)
    message = graphene.String()

    def mutate(self, info):
        low_stock_items = Product.objects.filter(stock__lt=10)
        names = []
        for product in low_stock_items:
            product.stock += 10
            product.save()
            names.append(product.name)
        
        return UpdateLowStockProducts(
            updated_products=names,
            message="Stock successfully updated for low-stock products."
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")
    total_stats = graphene.JSONString()

    def resolve_total_stats(self, info):
        return {
            "customers": Customer.objects.count(),
            "orders": Order.objects.count(),
            "revenue": Order.objects.aggregate(Sum('totalamount'))['totalamount__sum'] or 0
        }

schema = graphene.Schema(query=Query, mutation=Mutation)
