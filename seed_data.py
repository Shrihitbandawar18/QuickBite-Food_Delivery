from models import db, User, Restaurant, MenuItem

def seed_database():
    if Restaurant.query.first() is not None:
        return
    
    admin = User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    
    test_user = User(username='user', email='user@example.com')
    test_user.set_password('user123')
    db.session.add(test_user)
    
    restaurants_data = [
        {
            'name': 'Italian Bistro',
            'cuisine': 'Italian',
            'description': 'Authentic Italian cuisine with fresh pasta and wood-fired pizzas',
            'image_url': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
            'rating': 4.5
        },
        {
            'name': 'Sushi Palace',
            'cuisine': 'Japanese',
            'description': 'Fresh sushi and traditional Japanese dishes',
            'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800',
            'rating': 4.7
        },
        {
            'name': 'Burger House',
            'cuisine': 'American',
            'description': 'Gourmet burgers and classic American comfort food',
            'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800',
            'rating': 4.3
        },
        {
            'name': 'Spice Garden',
            'cuisine': 'Indian',
            'description': 'Traditional Indian curries and tandoori specialties',
            'image_url': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800',
            'rating': 4.6
        }
    ]
    
    for restaurant_data in restaurants_data:
        restaurant = Restaurant(**restaurant_data)
        db.session.add(restaurant)
        db.session.flush()
        
        if restaurant.name == 'Italian Bistro':
            menu_items = [
                {'name': 'Margherita Pizza', 'description': 'Classic tomato, mozzarella, and basil', 'price': 12.99, 'category': 'Pizza', 'image_url': 'https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=500', 'is_featured': True},
                {'name': 'Spaghetti Carbonara', 'description': 'Creamy pasta with bacon and parmesan', 'price': 14.99, 'category': 'Pasta', 'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=500', 'is_featured': True},
                {'name': 'Lasagna', 'description': 'Layered pasta with meat sauce and cheese', 'price': 15.99, 'category': 'Pasta', 'image_url': 'https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=500', 'is_featured': False},
            ]
        elif restaurant.name == 'Sushi Palace':
            menu_items = [
                {'name': 'California Roll', 'description': 'Crab, avocado, and cucumber roll', 'price': 8.99, 'category': 'Rolls', 'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=500', 'is_featured': True},
                {'name': 'Salmon Sashimi', 'description': 'Fresh sliced salmon', 'price': 16.99, 'category': 'Sashimi', 'image_url': 'https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=500', 'is_featured': True},
                {'name': 'Dragon Roll', 'description': 'Eel and cucumber with avocado on top', 'price': 13.99, 'category': 'Rolls', 'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=500', 'is_featured': False},
            ]
        elif restaurant.name == 'Burger House':
            menu_items = [
                {'name': 'Classic Cheeseburger', 'description': 'Beef patty with cheese, lettuce, tomato', 'price': 10.99, 'category': 'Burgers', 'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500', 'is_featured': True},
                {'name': 'BBQ Bacon Burger', 'description': 'Beef patty with BBQ sauce and crispy bacon', 'price': 12.99, 'category': 'Burgers', 'image_url': 'https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=500', 'is_featured': False},
                {'name': 'French Fries', 'description': 'Crispy golden fries', 'price': 4.99, 'category': 'Sides', 'image_url': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500', 'is_featured': False},
            ]
        else:
            menu_items = [
                {'name': 'Chicken Tikka Masala', 'description': 'Tender chicken in creamy tomato sauce', 'price': 13.99, 'category': 'Curry', 'image_url': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500', 'is_featured': True},
                {'name': 'Lamb Biryani', 'description': 'Aromatic rice with spiced lamb', 'price': 16.99, 'category': 'Rice', 'image_url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500', 'is_featured': False},
                {'name': 'Garlic Naan', 'description': 'Fresh baked bread with garlic', 'price': 3.99, 'category': 'Bread', 'image_url': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500', 'is_featured': False},
            ]
        
        for item_data in menu_items:
            item = MenuItem(restaurant_id=restaurant.id, **item_data)
            db.session.add(item)
    
    db.session.commit()
    print("Database seeded successfully!")
