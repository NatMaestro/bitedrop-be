# BiteDrop API - Complete Endpoints Documentation

**Base URL:** `https://bitedrop.onrender.com`

**API Documentation:**

- Swagger UI: https://bitedrop.onrender.com/swagger/
- ReDoc: https://bitedrop.onrender.com/redoc/

---

## 🔐 Authentication

All authenticated endpoints require JWT token in header:

```
Authorization: Bearer <your-jwt-token>
```

---

## 👤 User Management

### Authentication Endpoints

| Method | Endpoint                    | Description                     | Auth Required |
| ------ | --------------------------- | ------------------------------- | ------------- |
| POST   | `/api/users/register/`      | Register new user               | No            |
| POST   | `/api/users/login/`         | User login (returns JWT tokens) | No            |
| POST   | `/api/users/token/refresh/` | Refresh JWT access token        | No            |

### User Profile

| Method | Endpoint         | Description                           | Auth Required |
| ------ | ---------------- | ------------------------------------- | ------------- |
| GET    | `/api/users/me/` | Get current user profile              | Yes           |
| PUT    | `/api/users/me/` | Update current user profile           | Yes           |
| PATCH  | `/api/users/me/` | Partially update current user profile | Yes           |

### User Management (Admin Only)

| Method | Endpoint                 | Description           | Auth Required |
| ------ | ------------------------ | --------------------- | ------------- |
| GET    | `/api/users/users/`      | List all users        | Admin         |
| GET    | `/api/users/users/{id}/` | Get user details      | Admin         |
| PUT    | `/api/users/users/{id}/` | Update user           | Admin         |
| PATCH  | `/api/users/users/{id}/` | Partially update user | Admin         |
| DELETE | `/api/users/users/{id}/` | Delete user           | Admin         |

---

## 🍕 Restaurants

| Method | Endpoint                          | Description                 | Auth Required |
| ------ | --------------------------------- | --------------------------- | ------------- |
| GET    | `/api/restaurants/`               | List all restaurants        | No            |
| POST   | `/api/restaurants/`               | Create restaurant           | Admin         |
| GET    | `/api/restaurants/{id}/`          | Get restaurant details      | No            |
| PUT    | `/api/restaurants/{id}/`          | Update restaurant           | Admin         |
| PATCH  | `/api/restaurants/{id}/`          | Partially update restaurant | Admin         |
| DELETE | `/api/restaurants/{id}/`          | Delete restaurant           | Admin         |
| GET    | `/api/restaurants/{id}/products/` | Get restaurant products     | No            |
| GET    | `/api/restaurants/{id}/reviews/`  | Get restaurant reviews      | No            |

**Query Parameters:**

- `?is_partner=true` - Filter by partner status
- `?search=kfc` - Search by name/description
- `?ordering=rating` - Sort by rating
- `?ordering=-created_at` - Sort by newest first

---

## 🍔 Products

| Method | Endpoint                      | Description              | Auth Required |
| ------ | ----------------------------- | ------------------------ | ------------- |
| GET    | `/api/products/`              | List all products        | No            |
| POST   | `/api/products/`              | Create product           | Admin         |
| GET    | `/api/products/{id}/`         | Get product details      | No            |
| PUT    | `/api/products/{id}/`         | Update product           | Admin         |
| PATCH  | `/api/products/{id}/`         | Partially update product | Admin         |
| DELETE | `/api/products/{id}/`         | Delete product           | Admin         |
| GET    | `/api/products/flash_sale/`   | Get flash sale products  | No            |
| GET    | `/api/products/discounted/`   | Get discounted products  | No            |
| GET    | `/api/products/{id}/reviews/` | Get product reviews      | No            |

**Query Parameters:**

- `?restaurant={id}` - Filter by restaurant
- `?category={id}` - Filter by category
- `?is_flash_sale=true` - Filter flash sale items
- `?in_stock=true` - Filter in-stock items
- `?search=burger` - Search by name/description
- `?ordering=price` - Sort by price
- `?ordering=-rating` - Sort by highest rating

---

## 📂 Categories

| Method | Endpoint                | Description               | Auth Required |
| ------ | ----------------------- | ------------------------- | ------------- |
| GET    | `/api/categories/`      | List all categories       | No            |
| POST   | `/api/categories/`      | Create category           | Admin         |
| GET    | `/api/categories/{id}/` | Get category details      | No            |
| PUT    | `/api/categories/{id}/` | Update category           | Admin         |
| PATCH  | `/api/categories/{id}/` | Partially update category | Admin         |
| DELETE | `/api/categories/{id}/` | Delete category           | Admin         |

**Query Parameters:**

- `?is_active=true` - Filter active categories
- `?search=pizza` - Search by name

---

## 🛒 Orders

| Method | Endpoint                           | Description            | Auth Required |
| ------ | ---------------------------------- | ---------------------- | ------------- |
| GET    | `/api/orders/`                     | List user orders       | Yes           |
| POST   | `/api/orders/`                     | Create new order       | Yes           |
| GET    | `/api/orders/{id}/`                | Get order details      | Yes           |
| PUT    | `/api/orders/{id}/`                | Update order           | Yes           |
| PATCH  | `/api/orders/{id}/`                | Partially update order | Yes           |
| DELETE | `/api/orders/{id}/`                | Delete order           | Yes           |
| POST   | `/api/orders/{id}/cancel/`         | Cancel order           | Yes           |
| POST   | `/api/orders/{id}/confirm/`        | Confirm order          | Staff         |
| POST   | `/api/orders/{id}/mark_delivered/` | Mark as delivered      | Staff         |

**Query Parameters:**

- `?status=pending` - Filter by status (pending, confirmed, preparing, delivering, delivered, cancelled)
- `?payment_status=completed` - Filter by payment status
- `?payment_method=mobile_money` - Filter by payment method

---

## 🎯 Discounts

| Method | Endpoint                           | Description               | Auth Required |
| ------ | ---------------------------------- | ------------------------- | ------------- |
| GET    | `/api/discounts/`                  | List all discounts        | No            |
| POST   | `/api/discounts/`                  | Create discount           | Admin         |
| GET    | `/api/discounts/{id}/`             | Get discount details      | No            |
| PUT    | `/api/discounts/{id}/`             | Update discount           | Admin         |
| PATCH  | `/api/discounts/{id}/`             | Partially update discount | Admin         |
| DELETE | `/api/discounts/{id}/`             | Delete discount           | Admin         |
| GET    | `/api/discounts/active/`           | Get active discounts      | No            |
| GET    | `/api/discounts/global_discounts/` | Get global discounts      | No            |

**Query Parameters:**

- `?discount_type=percentage` - Filter by type (percentage, fixed)
- `?restaurant={id}` - Filter by restaurant
- `?is_active=true` - Filter active discounts

---

## ❤️ Favorites

| Method | Endpoint                      | Description              | Auth Required |
| ------ | ----------------------------- | ------------------------ | ------------- |
| GET    | `/api/favorites/`             | List user favorites      | Yes           |
| POST   | `/api/favorites/`             | Add to favorites         | Yes           |
| GET    | `/api/favorites/{id}/`        | Get favorite details     | Yes           |
| DELETE | `/api/favorites/{id}/`        | Remove from favorites    | Yes           |
| GET    | `/api/favorites/restaurants/` | Get favorite restaurants | Yes           |
| GET    | `/api/favorites/products/`    | Get favorite products    | Yes           |

**Query Parameters:**

- `?type=restaurant` - Filter by type (restaurant, product)

---

## 💰 Wallet & Transactions

| Method | Endpoint                             | Description                              | Auth Required |
| ------ | ------------------------------------ | ---------------------------------------- | ------------- |
| GET    | `/api/wallet-transactions/`          | List user transactions                   | Yes           |
| POST   | `/api/wallet-transactions/`          | Create transaction                       | Yes           |
| GET    | `/api/wallet-transactions/{id}/`     | Get transaction details                  | Yes           |
| GET    | `/api/wallet-transactions/balance/`  | Get wallet balance & recent transactions | Yes           |
| GET    | `/api/wallet-transactions/earned/`   | Get earned transactions                  | Yes           |
| GET    | `/api/wallet-transactions/redeemed/` | Get redeemed transactions                | Yes           |

**Query Parameters:**

- `?type=earned` - Filter by type (earned, redeemed, bonus, refund, top_up)

---

## 📱 Notifications

| Method | Endpoint                             | Description                   | Auth Required |
| ------ | ------------------------------------ | ----------------------------- | ------------- |
| GET    | `/api/notifications/`                | List user notifications       | Yes           |
| POST   | `/api/notifications/`                | Create notification           | Admin         |
| GET    | `/api/notifications/{id}/`           | Get notification details      | Yes           |
| PUT    | `/api/notifications/{id}/`           | Update notification           | Yes           |
| PATCH  | `/api/notifications/{id}/`           | Partially update notification | Yes           |
| DELETE | `/api/notifications/{id}/`           | Delete notification           | Yes           |
| GET    | `/api/notifications/unread/`         | Get unread notifications      | Yes           |
| POST   | `/api/notifications/mark_all_read/`  | Mark all as read              | Yes           |
| POST   | `/api/notifications/{id}/mark_read/` | Mark notification as read     | Yes           |

**Query Parameters:**

- `?is_read=false` - Filter by read status
- `?type=order_update` - Filter by type (welcome, order_update, promotion, payment, delivery, system)

---

## ⭐ Reviews

| Method | Endpoint                   | Description                       | Auth Required |
| ------ | -------------------------- | --------------------------------- | ------------- |
| GET    | `/api/reviews/`            | List all reviews                  | No            |
| POST   | `/api/reviews/`            | Create review                     | Yes           |
| GET    | `/api/reviews/{id}/`       | Get review details                | No            |
| PUT    | `/api/reviews/{id}/`       | Update review                     | Yes           |
| PATCH  | `/api/reviews/{id}/`       | Partially update review           | Yes           |
| DELETE | `/api/reviews/{id}/`       | Delete review                     | Yes           |
| GET    | `/api/reviews/my_reviews/` | Get user's reviews                | Yes           |
| GET    | `/api/reviews/high_rated/` | Get high-rated reviews (4+ stars) | No            |

**Query Parameters:**

- `?product={id}` - Filter by product
- `?restaurant={id}` - Filter by restaurant
- `?rating=5` - Filter by rating

---

## 🚚 Delivery Zones

| Method | Endpoint                    | Description                    | Auth Required |
| ------ | --------------------------- | ------------------------------ | ------------- |
| GET    | `/api/delivery-zones/`      | List all delivery zones        | No            |
| POST   | `/api/delivery-zones/`      | Create delivery zone           | Admin         |
| GET    | `/api/delivery-zones/{id}/` | Get delivery zone details      | No            |
| PUT    | `/api/delivery-zones/{id}/` | Update delivery zone           | Admin         |
| PATCH  | `/api/delivery-zones/{id}/` | Partially update delivery zone | Admin         |
| DELETE | `/api/delivery-zones/{id}/` | Delete delivery zone           | Admin         |

**Query Parameters:**

- `?is_active=true` - Filter active zones

---

## 💳 Payment Methods

| Method | Endpoint                     | Description                     | Auth Required |
| ------ | ---------------------------- | ------------------------------- | ------------- |
| GET    | `/api/payment-methods/`      | List all payment methods        | No            |
| POST   | `/api/payment-methods/`      | Create payment method           | Admin         |
| GET    | `/api/payment-methods/{id}/` | Get payment method details      | No            |
| PUT    | `/api/payment-methods/{id}/` | Update payment method           | Admin         |
| PATCH  | `/api/payment-methods/{id}/` | Partially update payment method | Admin         |
| DELETE | `/api/payment-methods/{id}/` | Delete payment method           | Admin         |

**Query Parameters:**

- `?type=mobile_money` - Filter by type (mobile_money, card, wallet, cash)
- `?is_active=true` - Filter active methods

---

## 📊 Pagination

All list endpoints support pagination:

- `?page=1` - Page number
- `?page_size=20` - Items per page (default: 20)

**Response Format:**

```json
{
  "count": 100,
  "next": "https://bitedrop.onrender.com/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 🔍 Search & Filtering

Most endpoints support:

- **Search**: `?search=term` - Search across relevant fields
- **Ordering**: `?ordering=field` or `?ordering=-field` (descending)
- **Filtering**: Various filters based on model fields

---

## 📝 Request/Response Examples

### User Registration

```javascript
POST /api/users/register/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "+233 24 123 4567",
  "address": "123 Main St, Accra, Ghana",
  "role": "user"
}

Response: 201 Created
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    ...
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### User Login

```javascript
POST /api/users/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "wallet_balance": "45.50",
    "loyalty_points": 1250
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Get Restaurants

```javascript
GET /api/restaurants/

Response: 200 OK
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "name": "KFC",
      "logo": "https://...",
      "description": "Finger Lickin' Good",
      "rating": "4.50",
      "delivery_time": "25-35 min",
      "cuisine_type": ["American", "Fast Food"],
      "is_partner": true,
      "delivery_fee": "5.00",
      "minimum_order": "15.00"
    }
  ]
}
```

### Get Products

```javascript
GET /api/products/?restaurant={id}

Response: 200 OK
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "name": "Zinger Burger Combo",
      "description": "Crispy zinger burger with fries and drink",
      "price": "12.99",
      "discount_price": "9.99",
      "discount_percentage": 23,
      "image": "https://...",
      "category": {
        "id": "uuid",
        "name": "Combos"
      },
      "restaurant": {
        "id": "uuid",
        "name": "KFC"
      },
      "in_stock": true,
      "is_flash_sale": true,
      "rating": "4.50",
      "reviews_count": 234
    }
  ]
}
```

### Create Order

```javascript
POST /api/orders/
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "delivery_address": "123 Main St, Accra, Ghana",
  "delivery_fee": 5.00,
  "payment_method": "mobile_money",
  "notes": "Please ring doorbell",
  "items": [
    {
      "product": "product-uuid",
      "quantity": 2,
      "unit_price": 9.99
    }
  ]
}

Response: 201 Created
{
  "id": "order-uuid",
  "user": {...},
  "total": "19.98",
  "status": "pending",
  "payment_status": "pending",
  "items": [...]
}
```

### Get User Orders

```javascript
GET /api/orders/
Authorization: Bearer <jwt-token>

Response: 200 OK
{
  "count": 3,
  "results": [
    {
      "id": "order-uuid",
      "user": {...},
      "total": "19.98",
      "status": "delivered",
      "payment_status": "completed",
      "delivery_address": "123 Main St, Accra, Ghana",
      "created_at": "2025-01-15T10:30:00Z",
      "items": [...]
    }
  ]
}
```

### Add to Favorites

```javascript
POST /api/favorites/
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
  "type": "restaurant",
  "restaurant": "restaurant-uuid"
}

// OR for product
{
  "type": "product",
  "product": "product-uuid"
}

Response: 201 Created
```

### Get Wallet Balance

```javascript
GET /api/wallet-transactions/balance/
Authorization: Bearer <jwt-token>

Response: 200 OK
{
  "wallet_balance": "45.50",
  "loyalty_points": 1250,
  "total_transactions": 15,
  "recent_transactions": [...]
}
```

### Get Notifications

```javascript
GET /api/notifications/unread/
Authorization: Bearer <jwt-token>

Response: 200 OK
{
  "count": 3,
  "results": [
    {
      "id": "notif-uuid",
      "title": "Order Delivered",
      "message": "Your order has been delivered successfully!",
      "type": "order_update",
      "is_read": false,
      "created_at": "2025-01-15T11:45:00Z"
    }
  ]
}
```

---

## 🚨 Error Responses

### 400 Bad Request

```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error."
}
```

---

## 🎯 Frontend Integration Tips

### 1. Store JWT Token

```javascript
// After login, store tokens
localStorage.setItem("access_token", response.tokens.access);
localStorage.setItem("refresh_token", response.tokens.refresh);
```

### 2. Add Token to Requests

```javascript
const token = localStorage.getItem("access_token");
fetch("https://bitedrop.onrender.com/api/orders/", {
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
});
```

### 3. Handle Token Refresh

```javascript
// When access token expires (401 error)
const refreshToken = localStorage.getItem("refresh_token");
fetch("https://bitedrop.onrender.com/api/users/token/refresh/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ refresh: refreshToken }),
});
```

### 4. Error Handling

```javascript
try {
  const response = await fetch(url, options);
  if (!response.ok) {
    if (response.status === 401) {
      // Redirect to login
    } else if (response.status === 403) {
      // Show permission error
    }
  }
  return await response.json();
} catch (error) {
  console.error("API Error:", error);
}
```

---

## 📊 Total Endpoints

- **Authentication**: 3 endpoints
- **User Management**: 8 endpoints
- **Restaurants**: 8 endpoints
- **Products**: 9 endpoints
- **Categories**: 6 endpoints
- **Orders**: 9 endpoints
- **Discounts**: 8 endpoints
- **Favorites**: 6 endpoints
- **Wallet**: 6 endpoints
- **Notifications**: 9 endpoints
- **Reviews**: 8 endpoints
- **Delivery Zones**: 6 endpoints
- **Payment Methods**: 6 endpoints

**Total: 92+ REST API Endpoints**

---

## 🎉 Ready for Frontend Integration!

Your BiteDrop API is fully functional and ready to power your food delivery platform.

For detailed request/response schemas, visit: https://bitedrop.onrender.com/swagger/
