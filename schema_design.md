# Food Ordering App - Initial Schema Design

## Table: users

Purpose:
Stores customer/admin account information.

Fields:

* id: UUID (Primary Key)
* full_name: String
* email: String (Unique, Indexed)
* phone_number: String (Unique)
* password_hash: String
* role: String

  * Example values:

    * customer
    * admin
    * restaurant_owner
* is_active: Boolean
* created_at: Timestamp
* updated_at: Timestamp

---

## Table: restaurants

Purpose:
Stores restaurant/shop information.

Fields:

* id: UUID (Primary Key)
* owner_id: UUID (Foreign Key → users.id)
* name: String (Indexed)
* description: Text
* phone_number: String
* address: Text
* township: String
* logo_url: String (Nullable)
* cover_image_url: String (Nullable)
* is_open: Boolean
* created_at: Timestamp
* updated_at: Timestamp

Relationship Notes:

* One user can own multiple restaurants.
* owner_id links restaurant → users table.

---

## Table: categories

Purpose:
Groups menu items into logical sections.

Examples:

* Drinks
* BBQ
* Dessert
* Rice

Fields:

* id: UUID (Primary Key)
* restaurant_id: UUID (Foreign Key → restaurants.id)
* name: String
* description: Text (Nullable)
* created_at: Timestamp

Relationship Notes:

* One restaurant can have many categories.
* restaurant_id links category → restaurant.

---

## Table: menu_items

Purpose:
Stores food/menu information.

Fields:

* id: UUID (Primary Key)
* restaurant_id: UUID (Foreign Key → restaurants.id)
* category_id: UUID (Foreign Key → categories.id)
* name: String (Indexed)
* description: Text
* price_mmk: Integer
* image_url: String (Nullable)
* is_available: Boolean
* preparation_time_minutes: Integer (Nullable)
* created_at: Timestamp
* updated_at: Timestamp

Relationship Notes:

* One restaurant can have many menu items.
* One category can contain many menu items.
* restaurant_id tells us which restaurant owns this menu item.
* category_id tells us which category this item belongs to.

Example:
"Chicken Fried Rice"
belongs to:

* restaurant_id → YKKO Restaurant
* category_id → Rice

---

## Table: orders

Purpose:
Stores finalized customer orders.

Fields:

* id: UUID (Primary Key)
* user_id: UUID (Foreign Key → users.id)
* restaurant_id: UUID (Foreign Key → restaurants.id)
* order_number: String (Unique, Indexed)
* order_status: String

  * Example values:

    * pending
    * confirmed
    * preparing
    * delivering
    * completed
    * cancelled
* total_amount_mmk: Integer
* delivery_address: Text
* customer_phone: String
* order_note: Text (Nullable)
* ordered_at: Timestamp
* updated_at: Timestamp

Relationship Notes:

* One user can create many orders.
* One restaurant can receive many orders.
* user_id links order → customer.
* restaurant_id links order → restaurant.

Important MMK Design Decision:

* price_mmk and total_amount_mmk use Integer.
* We do NOT use Decimal/Float because MMK does not require fractional currency handling in this project.

---

# Relationship Summary

users
└── restaurants
└── categories
└── menu_items

users
└── orders

restaurants
└── orders

---

# Architecture Notes

Why UUID instead of Integer IDs?

* Better for distributed systems
* Harder to guess
* Safer for public APIs

Why separate Category table?

* Cleaner filtering
* Easier frontend rendering
* Better scalability

Why separate Order from MenuItem?

* Menu prices may change later
* Orders must preserve historical purchase data

Why Integer for MMK?

* No decimal precision needed
* Simpler calculations
* Avoids floating-point currency issues
