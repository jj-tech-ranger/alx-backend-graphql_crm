import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order

def seed():
    Customer.objects.all().delete()
    Product.objects.all().delete()
    Order.objects.all().delete()

    c1 = Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
    c2 = Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")
    c3 = Customer.objects.create(name="Carol", email="carol@example.com")

    p1 = Product.objects.create(name="Laptop", price=999.99, stock=10)
    p2 = Product.objects.create(name="Mouse", price=25.50, stock=50)
    p3 = Product.objects.create(name="Keyboard", price=45.00, stock=30)

    o1 = Order.objects.create(customer=c1, total_amount=1025.49)
    o1.products.set([p1, p2])

    o2 = Order.objects.create(customer=c2, total_amount=45.00)
    o2.products.set([p3])

    print("Database seeded successfully.")

if __name__ == '__main__':
    seed()