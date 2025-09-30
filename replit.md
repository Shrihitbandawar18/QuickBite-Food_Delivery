# Food Delivery Application

## Overview

This is a Flask-based food delivery web application that allows users to browse restaurants, view menus, add items to cart, and place orders. The application includes an admin panel for managing restaurants, menu items, and viewing orders. The system uses SQLAlchemy ORM with SQLite for data persistence and implements session-based authentication with role-based access control.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- Base template pattern for consistent layout across all pages
- Component-based structure with reusable navigation and flash messaging
- Client-side interactivity handled through Bootstrap JavaScript components
- Custom CSS for enhanced styling and hover effects

**Key Design Patterns**:
- Template inheritance for DRY principle
- Flash messages for user feedback
- Session-based state management for cart functionality
- Responsive design with mobile-first approach

### Backend Architecture

**Web Framework**: Flask with Blueprint pattern for modular routing
- `auth_bp`: Handles user authentication (signup, login, logout)
- `main_bp`: Manages customer-facing features (browsing, cart, orders)
- `admin_bp`: Provides administrative CRUD operations with prefix `/admin`

**Authentication & Authorization**:
- Session-based authentication using Flask's session management
- Password hashing with Werkzeug's security utilities (generate_password_hash, check_password_hash)
- Role-based access control with `is_admin` flag
- Custom decorators (`@login_required`, `@admin_required`) for route protection

**Application Factory Pattern**: 
- `create_app()` function initializes Flask app, registers blueprints, and sets up database
- Automatic database initialization and seeding on startup
- Environment-based configuration (SECRET_KEY from environment variables)

### Data Architecture

**ORM**: SQLAlchemy with Flask-SQLAlchemy extension

**Database Schema**:

1. **User Model**
   - Fields: id, username, email, password_hash, is_admin, created_at
   - Relationships: One-to-many with Order
   - Methods: set_password(), check_password()

2. **Restaurant Model**
   - Fields: id, name, cuisine, description, image_url, rating, created_at
   - Relationships: One-to-many with MenuItem (cascade delete)
   - Purpose: Store restaurant information and metadata

3. **MenuItem Model**
   - Fields: id, name, description, price, category, image_url, restaurant_id, is_featured, created_at
   - Relationships: Many-to-one with Restaurant
   - Purpose: Store menu items linked to specific restaurants

4. **Order Model**
   - Fields: id, user_id, total_amount, status, delivery_address, phone, created_at
   - Relationships: Many-to-one with User, One-to-many with OrderItem
   - Purpose: Track customer orders

5. **OrderItem Model**
   - Fields: id, order_id, menu_item_id, quantity, price
   - Relationships: Many-to-one with Order and MenuItem
   - Purpose: Establish many-to-many relationship between orders and menu items

**Database Technology**: SQLite for development (connection string: `sqlite:///food_delivery.db`)
- Pros: Zero configuration, file-based, perfect for development and small deployments
- Cons: Limited concurrency, not suitable for high-traffic production
- Migration path: Can be replaced with PostgreSQL by changing SQLALCHEMY_DATABASE_URI

### External Dependencies

**Python Packages**:
- `Flask`: Core web framework
- `Flask-SQLAlchemy`: ORM integration
- `Werkzeug`: Password hashing and security utilities

**Frontend Libraries** (CDN):
- Bootstrap 5.3.0: UI framework for responsive design
- Bootstrap Icons 1.10.0: Icon library for UI elements

**Third-party Services**:
- Unsplash API: Used for restaurant and food images (image URLs in seed data)
- No payment gateway integration (currently cash-on-delivery only)

**Session Management**:
- Flask's built-in session with SECRET_KEY configuration
- Session stores: user_id, username, is_admin flag, shopping cart data
- Cart stored as dictionary in session: {item_id: quantity}

**Seeding Strategy**:
- Automatic database seeding on app startup via `seed_data.py`
- Creates default admin (username: admin, password: admin123) and test user accounts (username: user, password: user123)
- Populates 4 sample restaurants with Unsplash imagery
- Each restaurant includes 3 menu items with sample data
- Idempotent seeding (checks if data exists before inserting)

## Features Implemented

### User Features
1. **Authentication**: Sign up, login, logout with secure password hashing
2. **Browse Restaurants**: View all restaurants with cuisine types, ratings, and descriptions
3. **Featured Dishes**: Homepage displays featured menu items from various restaurants
4. **Restaurant Menu**: Detailed menu pages for each restaurant with categorized items
5. **Shopping Cart**: Add items to cart, update quantities, remove items
6. **Checkout**: Enter delivery address and phone number, view order summary
7. **Order Confirmation**: Confirmation page with order details and status

### Admin Features
1. **Dashboard**: Overview with statistics (restaurant count, menu item count, order count)
2. **Restaurant Management**: Add, edit, and delete restaurants
3. **Menu Item Management**: Add, edit, and delete menu items with restaurant association
4. **Order Management**: View all orders with customer details and order items
5. **Featured Items**: Mark menu items as featured to display on homepage

## Project Structure

```
/
├── app.py                  # Main Flask application with app factory
├── seed_data.py           # Database seeding with sample data
├── models/
│   └── __init__.py        # SQLAlchemy models (User, Restaurant, MenuItem, Order, OrderItem)
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Authentication routes (signup, login, logout)
│   ├── main.py            # Customer-facing routes (homepage, menu, cart, checkout)
│   └── admin.py           # Admin panel routes (restaurant/menu management, orders)
├── templates/
│   ├── base.html          # Base template with navigation and layout
│   ├── index.html         # Homepage with restaurants and featured dishes
│   ├── signup.html        # User registration form
│   ├── login.html         # Login form with demo credentials
│   ├── restaurant_menu.html  # Restaurant menu page
│   ├── cart.html          # Shopping cart with update/remove functionality
│   ├── checkout.html      # Checkout form with order summary
│   ├── order_confirmation.html  # Order confirmation page
│   └── admin/
│       ├── dashboard.html     # Admin dashboard with statistics
│       ├── restaurants.html   # Restaurant list and management
│       ├── add_restaurant.html   # Add new restaurant form
│       ├── edit_restaurant.html  # Edit restaurant form
│       ├── menu_items.html    # Menu items list and management
│       ├── add_menu_item.html    # Add new menu item form
│       ├── edit_menu_item.html   # Edit menu item form
│       └── orders.html        # View all orders
└── static/
    └── css/
        └── style.css      # Custom CSS with Bootstrap enhancements
```

## Known Limitations and Future Improvements

1. **Security**: No CSRF protection on POST routes (recommended to add Flask-WTF)
2. **Validation**: Admin form numeric fields lack input validation (could crash on invalid input)
3. **Testing**: No automated tests for authentication, cart, and checkout flows
4. **Payment**: Only supports cash-on-delivery (no payment gateway integration)
5. **Order Tracking**: Order status is static (no real-time updates or status changes)
6. **Search/Filter**: No search functionality for restaurants or menu items
7. **User Orders**: No page for users to view their order history

## How to Run

The application is configured with a Flask workflow that runs automatically. The server listens on port 5000.

**Demo Credentials**:
- Admin: username: `admin`, password: `admin123`
- User: username: `user`, password: `user123`

## Recent Changes

- **2025-09-30**: Complete implementation of food delivery website with all requested features
  - Set up Flask with blueprints architecture
  - Implemented SQLAlchemy models with proper relationships
  - Created authentication system with password hashing and session management
  - Built customer-facing features (homepage, menu browsing, cart, checkout)
  - Developed complete admin panel with CRUD operations
  - Added responsive Bootstrap 5 design with custom CSS
  - Created seed data with sample restaurants and menu items
