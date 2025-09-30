from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, Restaurant, MenuItem, Order, OrderItem
from functools import wraps

main_bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    restaurants = Restaurant.query.all()
    featured_items = MenuItem.query.filter_by(is_featured=True).limit(6).all()
    return render_template('index.html', restaurants=restaurants, featured_items=featured_items)

@main_bp.route('/restaurant/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template('restaurant_menu.html', restaurant=restaurant, menu_items=menu_items)

@main_bp.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', {})
    items = []
    total = 0
    
    for item_id, quantity in cart_items.items():
        menu_item = MenuItem.query.get(int(item_id))
        if menu_item:
            items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': quantity,
                'restaurant': menu_item.restaurant.name,
                'subtotal': menu_item.price * quantity
            })
            total += menu_item.price * quantity
    
    return render_template('cart.html', items=items, total=total)

@main_bp.route('/add_to_cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    cart = session.get('cart', {})
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        cart[item_id_str] += 1
    else:
        cart[item_id_str] = 1
    
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    quantity = int(request.form.get('quantity', 0))
    cart = session.get('cart', {})
    item_id_str = str(item_id)
    
    if quantity > 0:
        cart[item_id_str] = quantity
    elif item_id_str in cart:
        del cart[item_id_str]
    
    session['cart'] = cart
    return redirect(url_for('main.cart'))

@main_bp.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart = session.get('cart', {})
    item_id_str = str(item_id)
    
    if item_id_str in cart:
        del cart[item_id_str]
    
    session['cart'] = cart
    flash('Item removed from cart', 'info')
    return redirect(url_for('main.cart'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = session.get('cart', {})
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        items = []
        total = 0
        
        for item_id, quantity in cart_items.items():
            menu_item = MenuItem.query.get(int(item_id))
            if menu_item:
                items.append({
                    'menu_item': menu_item,
                    'quantity': quantity,
                    'subtotal': menu_item.price * quantity
                })
                total += menu_item.price * quantity
        
        order = Order(
            user_id=session['user_id'],
            total_amount=total,
            delivery_address=address,
            phone=phone
        )
        db.session.add(order)
        db.session.flush()
        
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item['menu_item'].id,
                quantity=item['quantity'],
                price=item['menu_item'].price
            )
            db.session.add(order_item)
        
        db.session.commit()
        session.pop('cart', None)
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.order_confirmation', order_id=order.id))
    
    items = []
    total = 0
    
    for item_id, quantity in cart_items.items():
        menu_item = MenuItem.query.get(int(item_id))
        if menu_item:
            items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': quantity,
                'subtotal': menu_item.price * quantity
            })
            total += menu_item.price * quantity
    
    return render_template('checkout.html', items=items, total=total)

@main_bp.route('/order_confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('order_confirmation.html', order=order)
