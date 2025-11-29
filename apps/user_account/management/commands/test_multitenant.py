"""
Management command to test multi-tenant functionality.
Tests that restaurant admins can only see/manage their own restaurant's data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.restaurant.models import Restaurant
from apps.product.models import Product
from apps.order.models import Order, OrderItem
from apps.discount.models import Discount
from apps.notification.models import Notification
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Test multi-tenant functionality for restaurant admins'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🧪 Testing Multi-Tenant Functionality...\n'))
        
        # Check if we have test data
        restaurants = Restaurant.objects.all()
        if restaurants.count() < 2:
            self.stdout.write(self.style.WARNING(
                '⚠️  Need at least 2 restaurants for testing. Creating test data...'
            ))
            self.create_test_data()
        
        # Test 1: Product Filtering
        self.test_product_filtering()
        
        # Test 2: Order Filtering
        self.test_order_filtering()
        
        # Test 3: Discount Filtering
        self.test_discount_filtering()
        
        # Test 4: Product Creation Enforcement
        self.test_product_creation_enforcement()
        
        # Test 5: Order Notifications
        self.test_order_notifications()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Multi-Tenant Testing Complete!\n'))

    def create_test_data(self):
        """Create test restaurants and users if they don't exist"""
        # Create Restaurant 1
        restaurant1, created = Restaurant.objects.get_or_create(
            name="Test Restaurant 1",
            defaults={
                'address': '123 Test St',
                'phone': '1234567890',
                'email': 'restaurant1@test.com',
            }
        )
        
        # Create Restaurant 2
        restaurant2, created = Restaurant.objects.get_or_create(
            name="Test Restaurant 2",
            defaults={
                'address': '456 Test Ave',
                'phone': '0987654321',
                'email': 'restaurant2@test.com',
            }
        )
        
        # Create Restaurant Admin 1
        admin1, created = User.objects.get_or_create(
            email='admin1@test.com',
            defaults={
                'name': 'Restaurant Admin 1',
                'role': 'restaurant_admin',
                'restaurant': restaurant1,
            }
        )
        if created:
            admin1.set_password('testpass123')
            admin1.save()
        
        # Create Restaurant Admin 2
        admin2, created = User.objects.get_or_create(
            email='admin2@test.com',
            defaults={
                'name': 'Restaurant Admin 2',
                'role': 'restaurant_admin',
                'restaurant': restaurant2,
            }
        )
        if created:
            admin2.set_password('testpass123')
            admin2.save()
        
        self.stdout.write(self.style.SUCCESS('✅ Test data created'))

    def test_product_filtering(self):
        """Test that restaurant admins only see their restaurant's products"""
        self.stdout.write('\n📦 Testing Product Filtering...')
        
        restaurant1 = Restaurant.objects.first()
        restaurant2 = Restaurant.objects.exclude(id=restaurant1.id).first()
        
        if not restaurant1 or not restaurant2:
            self.stdout.write(self.style.ERROR('❌ Need at least 2 restaurants'))
            return
        
        admin1 = User.objects.filter(role='restaurant_admin', restaurant=restaurant1).first()
        admin2 = User.objects.filter(role='restaurant_admin', restaurant=restaurant2).first()
        
        if not admin1 or not admin2:
            self.stdout.write(self.style.ERROR('❌ Need restaurant admins'))
            return
        
        # Create test products
        product1, _ = Product.objects.get_or_create(
            name='Product 1 - Restaurant 1',
            restaurant=restaurant1,
            defaults={
                'price': Decimal('10.00'),
                'description': 'Test product for restaurant 1',
            }
        )
        
        product2, _ = Product.objects.get_or_create(
            name='Product 2 - Restaurant 2',
            restaurant=restaurant2,
            defaults={
                'price': Decimal('20.00'),
                'description': 'Test product for restaurant 2',
            }
        )
        
        # Simulate filtering (as ViewSet would do)
        from apps.product.views import ProductViewSet
        from rest_framework.test import APIRequestFactory
        
        factory = APIRequestFactory()
        
        # Test Admin 1 sees only Restaurant 1 products
        request1 = factory.get('/api/products/')
        request1.user = admin1
        viewset1 = ProductViewSet()
        viewset1.request = request1
        queryset1 = viewset1.get_queryset()
        
        # Test Admin 2 sees only Restaurant 2 products
        request2 = factory.get('/api/products/')
        request2.user = admin2
        viewset2 = ProductViewSet()
        viewset2.request = request2
        queryset2 = viewset2.get_queryset()
        
        # Verify
        admin1_products = list(queryset1)
        admin2_products = list(queryset2)
        
        admin1_has_product1 = product1 in admin1_products
        admin1_has_product2 = product2 in admin1_products
        admin2_has_product1 = product1 in admin2_products
        admin2_has_product2 = product2 in admin2_products
        
        if admin1_has_product1 and not admin1_has_product2:
            self.stdout.write(self.style.SUCCESS('  ✅ Admin 1 sees only Restaurant 1 products'))
        else:
            self.stdout.write(self.style.ERROR(f'  ❌ Admin 1 filtering failed: has product1={admin1_has_product1}, has product2={admin1_has_product2}'))
        
        if admin2_has_product2 and not admin2_has_product1:
            self.stdout.write(self.style.SUCCESS('  ✅ Admin 2 sees only Restaurant 2 products'))
        else:
            self.stdout.write(self.style.ERROR(f'  ❌ Admin 2 filtering failed: has product1={admin2_has_product1}, has product2={admin2_has_product2}'))

    def test_order_filtering(self):
        """Test that restaurant admins only see orders with their products"""
        self.stdout.write('\n📋 Testing Order Filtering...')
        
        restaurant1 = Restaurant.objects.first()
        restaurant2 = Restaurant.objects.exclude(id=restaurant1.id).first()
        
        if not restaurant1 or not restaurant2:
            self.stdout.write(self.style.ERROR('❌ Need at least 2 restaurants'))
            return
        
        admin1 = User.objects.filter(role='restaurant_admin', restaurant=restaurant1).first()
        
        if not admin1:
            self.stdout.write(self.style.ERROR('❌ Need restaurant admin'))
            return
        
        # Create test customer
        customer, _ = User.objects.get_or_create(
            email='customer@test.com',
            defaults={
                'name': 'Test Customer',
                'role': 'user',
            }
        )
        
        # Create products
        product1 = Product.objects.filter(restaurant=restaurant1).first()
        product2 = Product.objects.filter(restaurant=restaurant2).first()
        
        if not product1 or not product2:
            self.stdout.write(self.style.WARNING('  ⚠️  Need products to test orders'))
            return
        
        # Create orders
        order1, _ = Order.objects.get_or_create(
            user=customer,
            defaults={
                'total': Decimal('10.00'),
                'delivery_address': '123 Test St',
                'payment_method': 'cash',
                'status': 'pending',
            }
        )
        
        # Add product from restaurant1 to order1
        if not order1.items.filter(product=product1).exists():
            OrderItem.objects.create(
                order=order1,
                product=product1,
                quantity=1,
                unit_price=product1.price,
                total_price=product1.price,
            )
        
        order2, _ = Order.objects.get_or_create(
            user=customer,
            defaults={
                'total': Decimal('20.00'),
                'delivery_address': '456 Test Ave',
                'payment_method': 'cash',
                'status': 'pending',
            }
        )
        
        # Add product from restaurant2 to order2
        if not order2.items.filter(product=product2).exists():
            OrderItem.objects.create(
                order=order2,
                product=product2,
                quantity=1,
                unit_price=product2.price,
                total_price=product2.price,
            )
        
        # Test filtering
        from apps.order.views import OrderViewSet
        from rest_framework.test import APIRequestFactory
        
        factory = APIRequestFactory()
        request = factory.get('/api/orders/')
        request.user = admin1
        viewset = OrderViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()
        
        admin1_orders = list(queryset)
        has_order1 = order1 in admin1_orders
        has_order2 = order2 in admin1_orders
        
        if has_order1 and not has_order2:
            self.stdout.write(self.style.SUCCESS('  ✅ Admin 1 sees only orders with Restaurant 1 products'))
        else:
            self.stdout.write(self.style.ERROR(f'  ❌ Order filtering failed: has order1={has_order1}, has order2={has_order2}'))

    def test_discount_filtering(self):
        """Test that restaurant admins only see their discounts + global discounts"""
        self.stdout.write('\n🎯 Testing Discount Filtering...')
        
        restaurant1 = Restaurant.objects.first()
        restaurant2 = Restaurant.objects.exclude(id=restaurant1.id).first()
        
        if not restaurant1 or not restaurant2:
            self.stdout.write(self.style.ERROR('❌ Need at least 2 restaurants'))
            return
        
        admin1 = User.objects.filter(role='restaurant_admin', restaurant=restaurant1).first()
        
        if not admin1:
            self.stdout.write(self.style.ERROR('❌ Need restaurant admin'))
            return
        
        # Create discounts
        from django.utils import timezone
        from datetime import timedelta
        
        discount1, _ = Discount.objects.get_or_create(
            name='Restaurant 1 Discount',
            restaurant=restaurant1,
            defaults={
                'discount_type': 'percentage',
                'discount_value': Decimal('10.00'),
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=30),
                'is_active': True,
            }
        )
        
        discount2, _ = Discount.objects.get_or_create(
            name='Restaurant 2 Discount',
            restaurant=restaurant2,
            defaults={
                'discount_type': 'percentage',
                'discount_value': Decimal('20.00'),
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=30),
                'is_active': True,
            }
        )
        
        global_discount, _ = Discount.objects.get_or_create(
            name='Global Discount',
            restaurant=None,
            defaults={
                'discount_type': 'percentage',
                'discount_value': Decimal('5.00'),
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=30),
                'is_active': True,
            }
        )
        
        # Test filtering
        from apps.discount.views import DiscountViewSet
        from rest_framework.test import APIRequestFactory
        
        factory = APIRequestFactory()
        request = factory.get('/api/discounts/')
        request.user = admin1
        viewset = DiscountViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()
        
        admin1_discounts = list(queryset)
        has_discount1 = discount1 in admin1_discounts
        has_discount2 = discount2 in admin1_discounts
        has_global = global_discount in admin1_discounts
        
        if has_discount1 and not has_discount2 and has_global:
            self.stdout.write(self.style.SUCCESS('  ✅ Admin 1 sees Restaurant 1 discounts + global discounts'))
        else:
            self.stdout.write(self.style.ERROR(
                f'  ❌ Discount filtering failed: has discount1={has_discount1}, '
                f'has discount2={has_discount2}, has global={has_global}'
            ))

    def test_product_creation_enforcement(self):
        """Test that restaurant admins can only create products for their restaurant"""
        self.stdout.write('\n🔒 Testing Product Creation Enforcement...')
        
        restaurant1 = Restaurant.objects.first()
        admin1 = User.objects.filter(role='restaurant_admin', restaurant=restaurant1).first()
        
        if not admin1 or not restaurant1:
            self.stdout.write(self.style.ERROR('❌ Need restaurant admin and restaurant'))
            return
        
        # Test that perform_create enforces restaurant assignment
        from apps.product.views import ProductViewSet
        from apps.product.serializers import ProductCreateUpdateSerializer
        from rest_framework.test import APIRequestFactory
        
        factory = APIRequestFactory()
        request = factory.post('/api/products/', {
            'name': 'Test Product',
            'price': '15.00',
            'description': 'Test',
        })
        request.user = admin1
        
        viewset = ProductViewSet()
        viewset.request = request
        
        serializer = ProductCreateUpdateSerializer(data={
            'name': 'Test Product Enforcement',
            'price': '15.00',
            'description': 'Test enforcement',
        })
        
        if serializer.is_valid():
            viewset.perform_create(serializer)
            product = serializer.instance
            
            if product.restaurant == restaurant1:
                self.stdout.write(self.style.SUCCESS('  ✅ Product automatically assigned to admin\'s restaurant'))
            else:
                self.stdout.write(self.style.ERROR(f'  ❌ Product assigned to wrong restaurant: {product.restaurant}'))
        else:
            self.stdout.write(self.style.ERROR(f'  ❌ Serializer validation failed: {serializer.errors}'))

    def test_order_notifications(self):
        """Test that restaurants receive notifications when orders are placed"""
        self.stdout.write('\n🔔 Testing Order Notifications...')
        
        restaurant1 = Restaurant.objects.first()
        admin1 = User.objects.filter(role='restaurant_admin', restaurant=restaurant1).first()
        
        if not admin1 or not restaurant1:
            self.stdout.write(self.style.ERROR('❌ Need restaurant admin and restaurant'))
            return
        
        # Count notifications before
        notifications_before = Notification.objects.filter(user=admin1).count()
        
        # Create customer
        customer, _ = User.objects.get_or_create(
            email='customer2@test.com',
            defaults={
                'name': 'Test Customer 2',
                'role': 'user',
            }
        )
        
        # Create product
        product = Product.objects.filter(restaurant=restaurant1).first()
        if not product:
            self.stdout.write(self.style.WARNING('  ⚠️  Need product to test notifications'))
            return
        
        # Create order (this should trigger notification)
        order = Order.objects.create(
            user=customer,
            total=Decimal('10.00'),
            delivery_address='123 Test St',
            payment_method='cash',
            status='pending',
        )
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            unit_price=product.price,
            total_price=product.price,
        )
        
        # Count notifications after
        notifications_after = Notification.objects.filter(user=admin1).count()
        
        if notifications_after > notifications_before:
            self.stdout.write(self.style.SUCCESS('  ✅ Restaurant admin received order notification'))
        else:
            self.stdout.write(self.style.ERROR('  ❌ No notification created for restaurant admin'))


