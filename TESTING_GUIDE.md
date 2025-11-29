# Multi-Tenant Testing Guide

## 🧪 Quick Test Command

Run this command from the `bitedrop-dj-be` directory:

```bash
python manage.py test_multitenant
```

This will automatically test:
1. ✅ Product filtering (restaurant admins see only their products)
2. ✅ Order filtering (restaurant admins see only their orders)
3. ✅ Discount filtering (restaurant admins see their discounts + global)
4. ✅ Product creation enforcement (auto-assigns to restaurant)
5. ✅ Order notifications (restaurants get notified)

---

## 📋 Manual Testing Steps

### Test 1: Product Filtering

1. **Create two restaurants:**
   ```python
   # In Django shell: python manage.py shell
   from apps.restaurant.models import Restaurant
   from apps.user_account.models import User
   
   r1 = Restaurant.objects.create(name="Restaurant 1", address="123 St", phone="123", email="r1@test.com")
   r2 = Restaurant.objects.create(name="Restaurant 2", address="456 Ave", phone="456", email="r2@test.com")
   ```

2. **Create restaurant admins:**
   ```python
   admin1 = User.objects.create_user(
       email="admin1@test.com",
       name="Admin 1",
       password="test123",
       role="restaurant_admin",
       restaurant=r1
   )
   
   admin2 = User.objects.create_user(
       email="admin2@test.com",
       name="Admin 2",
       password="test123",
       role="restaurant_admin",
       restaurant=r2
   )
   ```

3. **Create products for each restaurant:**
   ```python
   from apps.product.models import Product
   
   p1 = Product.objects.create(name="Product 1", price=10.00, restaurant=r1)
   p2 = Product.objects.create(name="Product 2", price=20.00, restaurant=r2)
   ```

4. **Test via API:**
   ```bash
   # Login as admin1
   curl -X POST http://localhost:8000/api/users/login/ \
     -H "Content-Type: application/json" \
     -d '{"email":"admin1@test.com","password":"test123"}'
   # Save the access token
   
   # Get products as admin1 (should only see Product 1)
   curl http://localhost:8000/api/products/ \
     -H "Authorization: Bearer <access_token>"
   ```

**Expected:** Admin1 should only see Product 1, not Product 2.

---

### Test 2: Order Filtering

1. **Create a customer and place orders:**
   ```python
   from apps.order.models import Order, OrderItem
   
   customer = User.objects.create_user(
       email="customer@test.com",
       name="Customer",
       password="test123",
       role="user"
   )
   
   # Order with Restaurant 1 product
   order1 = Order.objects.create(
       user=customer,
       total=10.00,
       delivery_address="123 St",
       payment_method="cash"
   )
   OrderItem.objects.create(order=order1, product=p1, quantity=1, unit_price=10.00, total_price=10.00)
   
   # Order with Restaurant 2 product
   order2 = Order.objects.create(
       user=customer,
       total=20.00,
       delivery_address="456 Ave",
       payment_method="cash"
   )
   OrderItem.objects.create(order=order2, product=p2, quantity=1, unit_price=20.00, total_price=20.00)
   ```

2. **Test via API:**
   ```bash
   # Get orders as admin1 (should only see order1)
   curl http://localhost:8000/api/orders/ \
     -H "Authorization: Bearer <admin1_access_token>"
   ```

**Expected:** Admin1 should only see order1, not order2.

---

### Test 3: Discount Filtering

1. **Create discounts:**
   ```python
   from apps.discount.models import Discount
   from django.utils import timezone
   from datetime import timedelta
   
   # Restaurant 1 discount
   d1 = Discount.objects.create(
       name="Restaurant 1 Discount",
       restaurant=r1,
       discount_type="percentage",
       discount_value=10.00,
       start_date=timezone.now(),
       end_date=timezone.now() + timedelta(days=30)
   )
   
   # Restaurant 2 discount
   d2 = Discount.objects.create(
       name="Restaurant 2 Discount",
       restaurant=r2,
       discount_type="percentage",
       discount_value=20.00,
       start_date=timezone.now(),
       end_date=timezone.now() + timedelta(days=30)
   )
   
   # Global discount
   d_global = Discount.objects.create(
       name="Global Discount",
       restaurant=None,
       discount_type="percentage",
       discount_value=5.00,
       start_date=timezone.now(),
       end_date=timezone.now() + timedelta(days=30)
   )
   ```

2. **Test via API:**
   ```bash
   # Get discounts as admin1 (should see d1 and d_global, not d2)
   curl http://localhost:8000/api/discounts/ \
     -H "Authorization: Bearer <admin1_access_token>"
   ```

**Expected:** Admin1 should see Restaurant 1 discount + Global discount, but NOT Restaurant 2 discount.

---

### Test 4: Product Creation Enforcement

1. **Create product as admin1:**
   ```bash
   curl -X POST http://localhost:8000/api/products/ \
     -H "Authorization: Bearer <admin1_access_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "New Product",
       "price": "15.00",
       "description": "Test product"
     }'
   ```

2. **Check the created product:**
   ```bash
   curl http://localhost:8000/api/products/<product_id>/ \
     -H "Authorization: Bearer <admin1_access_token>"
   ```

**Expected:** The product should automatically have `restaurant` set to Restaurant 1 (admin1's restaurant), even if not specified in the request.

---

### Test 5: Order Notifications

1. **Place an order:**
   ```bash
   # Login as customer
   curl -X POST http://localhost:8000/api/users/login/ \
     -H "Content-Type: application/json" \
     -d '{"email":"customer@test.com","password":"test123"}'
   
   # Place order
   curl -X POST http://localhost:8000/api/orders/ \
     -H "Authorization: Bearer <customer_access_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "delivery_address": "123 Test St",
       "delivery_fee": "2.00",
       "payment_method": "cash",
       "items": [
         {"product": "<p1_id>", "quantity": 1, "unit_price": "10.00"}
       ]
     }'
   ```

2. **Check notifications:**
   ```bash
   # Get notifications as admin1
   curl http://localhost:8000/api/notifications/ \
     -H "Authorization: Bearer <admin1_access_token>"
   ```

**Expected:** Admin1 should receive a notification about the new order.

---

## 🐛 Troubleshooting

### Issue: Test command not found
**Solution:** Make sure you're in the `bitedrop-dj-be` directory and Django is installed.

### Issue: No restaurants/users for testing
**Solution:** The test command will create test data automatically if needed.

### Issue: Notifications not created
**Solution:** 
1. Check that signals are registered in `apps/order/apps.py`
2. Verify the order was created with status='pending'
3. Check that the restaurant has admin/staff users

### Issue: Filtering not working
**Solution:**
1. Verify user has `restaurant` field set
2. Verify user role is `restaurant_admin` or `staff`
3. Check that products/orders are linked to the restaurant

---

## ✅ Success Criteria

All tests should pass:
- ✅ Restaurant admins see only their products
- ✅ Restaurant admins see only their orders
- ✅ Restaurant admins see their discounts + global discounts
- ✅ Products automatically assigned to restaurant on creation
- ✅ Restaurants receive order notifications

If all tests pass, the multi-tenant backend is working correctly! 🎉


