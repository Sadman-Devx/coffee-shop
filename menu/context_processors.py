def cart_context(request):
    """Make cart count available in all templates"""
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 0) for item in cart.values())
    return {'cart_count': cart_count}

