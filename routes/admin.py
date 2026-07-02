from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Restaurant, MenuItem, Order
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('auth.login'))
        if not session.get('is_admin'):
            flash('Admin access required', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    restaurant_count = Restaurant.query.count()
    menu_item_count = MenuItem.query.count()
    order_count = Order.query.count()
    return render_template('admin/dashboard.html', 
                         restaurant_count=restaurant_count,
                         menu_item_count=menu_item_count,
                         order_count=order_count)

@admin_bp.route('/restaurants')
@admin_required
def restaurants():
    restaurants = Restaurant.query.all()
    return render_template('admin/restaurants.html', restaurants=restaurants)

@admin_bp.route('/restaurant/add', methods=['GET', 'POST'])
@admin_required
def add_restaurant():
    if request.method == 'POST':
        restaurant = Restaurant(
            name=request.form.get('name'),
            cuisine=request.form.get('cuisine'),
            description=request.form.get('description'),
            image_url=request.form.get('image_url'),
            rating=float(request.form.get('rating', 4.0))
        )
        db.session.add(restaurant)
        db.session.commit()
        flash('Restaurant added successfully!', 'success')
        return redirect(url_for('admin.restaurants'))
    
    return render_template('admin/add_restaurant.html')

@admin_bp.route('/restaurant/edit/<int:restaurant_id>', methods=['GET', 'POST'])
@admin_required
def edit_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    if request.method == 'POST':
        restaurant.name = request.form.get('name')
        restaurant.cuisine = request.form.get('cuisine')
        restaurant.description = request.form.get('description')
        restaurant.image_url = request.form.get('image_url')
        restaurant.rating = float(request.form.get('rating', 4.0))
        db.session.commit()
        flash('Restaurant updated successfully!', 'success')
        return redirect(url_for('admin.restaurants'))
    
    return render_template('admin/edit_restaurant.html', restaurant=restaurant)

@admin_bp.route('/restaurant/delete/<int:restaurant_id>', methods=['POST'])
@admin_required
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    db.session.delete(restaurant)
    db.session.commit()
    flash('Restaurant deleted successfully!', 'success')
    return redirect(url_for('admin.restaurants'))

@admin_bp.route('/menu_items')
@admin_required
def menu_items():
    menu_items = MenuItem.query.all()
    return render_template('admin/menu_items.html', menu_items=menu_items)

@admin_bp.route('/menu_item/add', methods=['GET', 'POST'])
@admin_required
def add_menu_item():
    if request.method == 'POST':
        menu_item = MenuItem(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category'),
            image_url=request.form.get('image_url'),
            restaurant_id=int(request.form.get('restaurant_id')),
            is_featured=bool(request.form.get('is_featured'))
        )
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('admin.menu_items'))
    
    restaurants = Restaurant.query.all()
    return render_template('admin/add_menu_item.html', restaurants=restaurants)

@admin_bp.route('/menu_item/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_required
def edit_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        menu_item.name = request.form.get('name')
        menu_item.description = request.form.get('description')
        menu_item.price = float(request.form.get('price'))
        menu_item.category = request.form.get('category')
        menu_item.image_url = request.form.get('image_url')
        menu_item.restaurant_id = int(request.form.get('restaurant_id'))
        menu_item.is_featured = bool(request.form.get('is_featured'))
        db.session.commit()
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('admin.menu_items'))
    
    restaurants = Restaurant.query.all()
    return render_template('admin/edit_menu_item.html', menu_item=menu_item, restaurants=restaurants)

@admin_bp.route('/menu_item/delete/<int:item_id>', methods=['POST'])
@admin_required
def delete_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    db.session.delete(menu_item)
    db.session.commit()
    flash('Menu item deleted successfully!', 'success')
    return redirect(url_for('admin.menu_items'))

@admin_bp.route('/orders')
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@admin_bp.route('/orders/<int:order_id>/<status>')
@admin_required
def update_order_status(order_id, status):

    order = Order.query.get_or_404(order_id)

    valid_statuses = [
        "Pending",
        "Preparing",
        "Out for Delivery",
        "Delivered"
    ]

    if status not in valid_statuses:
        flash("Invalid order status!", "danger")
        return redirect(url_for('admin.orders'))

    order.status = status
    db.session.commit()

    flash(f"Order #{order.id} status updated to '{status}'.", "success")

    return redirect(url_for('admin.orders'))