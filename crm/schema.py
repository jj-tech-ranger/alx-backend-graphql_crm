import graphene
import re
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Sum
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node, )

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node, )

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node, )

class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int()

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()

class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, input):
        if Customer.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")

        if input.phone:
            if not re.match(r'^\+?1?\d{9,15}$|^\d{3}-\d{3}-\d{4}$', input.phone):
                raise Exception("Invalid phone format")

        customer = Customer.objects.create(
            name=input.name,
            email=input.email,
            phone=input.phone
        )
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        created_customers = []
        errors = []

        for cust_data in input:
            try:
                if Customer.objects.filter(email=cust_data.email).exists():
                    raise Exception(f"Email {cust_data.email} already exists")

                if cust_data.phone and not re.match(r'^\+?1?\d{9,15}$|^\d{3}-\d{3}-\d{4}$', cust_data.phone):
                    raise Exception(f"Invalid phone format for {cust_data.email}")

                customer = Customer.objects.create(
                    name=cust_data.name,
                    email=cust_data.email,
                    phone=cust_data.phone
                )
                created_customers.append(customer)
            except Exception as e:
                errors.append(str(e))

        return BulkCreateCustomers(customers=created_customers, errors=errors)

class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be positive")
        if input.stock is not None and input.stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=input.stock if input.stock is not None else 0
        )
        return CreateProduct(product=product)

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, input):
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        if not input.product_ids:
            raise Exception("At least one product must be selected")

        products = Product.objects.filter(pk__in=input.product_ids)
        if len(products) != len(input.product_ids):
            raise Exception("One or more invalid product IDs")

        total_amount = sum(product.price for product in products)

        order = Order(
            customer=customer,
            total_amount=total_amount
        )
        if input.order_date:
            order.order_date = input.order_date
        order.save()
        order.products.set(products)

        return CreateOrder(order=order)

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
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")
    total_stats = graphene.JSONString()
    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)

    def resolve_total_stats(self, info):
        return {
            "customers": Customer.objects.count(),
            "orders": Order.objects.count(),
            "revenue": Order.objects.aggregate(Sum('totalamount'))['totalamount__sum'] or 0
        }