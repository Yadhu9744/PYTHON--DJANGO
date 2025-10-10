from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from store.models import Product
from .models import Cart, Order, OrderItem

@login_required
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)  
    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def place_order(request):
    if request.method != "POST":
        return redirect('checkout')

    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')

    total = sum(item.total_price for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total)

    
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()
    return redirect('my_orders')





@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, product_id):
    item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    item.delete()
    return redirect('cart')