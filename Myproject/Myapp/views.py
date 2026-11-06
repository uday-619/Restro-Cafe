import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import SeatReservation, MenuItem, Order

# Helper to populate MenuItem table if empty or needs update
def populate_menu():
    # If we already have the new categories, we're good
    if MenuItem.objects.filter(category='Hot Beverages').count() > 0:
        return
        
    # Clear old database menu items to repopulate with description and availability fields
    MenuItem.objects.all().delete()
    
    items = [
        # Hot Beverages (Coffee Section)
        ('Espresso', 3.00, 'Hot Beverages', 'images/espresso.jpg', '100% Arabica dark roast espresso beans, extracted under high pressure for a thick, golden crema.', True),
        ('Americano', 3.50, 'Hot Beverages', 'images/americano.png', 'A bold, double-espresso shot diluted with hot purified water for a smooth black coffee flavor.', True),
        ('Cappuccino', 4.00, 'Hot Beverages', 'images/cappuccino.png', 'Equal parts of intense espresso, velvety steamed whole milk, and dense micro-milk foam.', True),
        ('Latte', 4.25, 'Hot Beverages', 'images/latte.png', 'A double espresso shot topped with creamy steamed milk and a delicate layer of milk foam.', True),
        ('Macchiato', 4.00, 'Hot Beverages', 'images/macchiato.png', 'Bold espresso marked with a single dollop of sweet, dense steamed milk foam.', True),
        ('Mocha', 4.50, 'Hot Beverages', 'images/mocha.png', 'Intense espresso blended with rich dark cocoa fudge sauce, steamed milk, and fresh whipped cream.', True),
        ('Flat White', 4.25, 'Hot Beverages', 'images/flat-white.png', 'Double shot of ristretto espresso topped with velvety whole milk microfoam for a smooth, punchy taste.', True),
        ('Long Black', 3.50, 'Hot Beverages', 'images/long-black.png', 'A double espresso shot extracted directly over hot water, preserving the creamy aromatic crema.', True),
        ('Matcha Latte', 4.75, 'Hot Beverages', 'images/matcha-latte.png', 'Premium-grade Japanese Uji matcha green tea powder whisked with steamed sweet whole milk.', True),

        # Cold Beverages (Coffee Section)
        ('Cold Coffee', 4.25, 'Cold Beverages', 'images/cold-coffee.png', 'Classic blended beverage made with sweet cold milk, double espresso shots, and vanilla ice cream.', True),
        ('Iced Coffee', 3.75, 'Cold Beverages', 'images/iced-coffee.png', 'Freshly brewed house coffee served chilled over ice cubes with a splash of milk.', True),
        ('Frappe', 4.95, 'Cold Beverages', 'images/frappe.png', 'Rich blended ice coffee made with milk, double espresso, and sweet vanilla syrup, finished with whipped cream.', True),
        ('Cold Brew', 4.50, 'Cold Beverages', 'images/cold-brew.png', 'Premium coarsely ground coffee beans steeped in cold water for 18 hours for a sweet, low-acid finish.', True),
        ('Iced Mocha', 4.75, 'Cold Beverages', 'images/iced-mocha.png', 'Chilled espresso combined with premium chocolate syrup, cold milk, ice, and whipped cream.', True),
        ('Caramel Coffee', 4.95, 'Cold Beverages', 'images/caramel-coffee.png', 'Blended iced coffee flavored with buttery caramel syrup, cold milk, and caramel drizzle.', True),
        ('Iced Latte', 4.25, 'Cold Beverages', 'images/iced-latte.png', 'Bold double shot of espresso and cold milk served over fresh ice cubes.', True),
        ('Honey Almond Coffee', 4.95, 'Cold Beverages', 'images/honey-almond-coffee.png', 'A refreshing blend of espresso, cold almond milk, and raw honey, shaken together with ice.', True),
        ('Chocolate Cold Coffee', 4.75, 'Cold Beverages', 'images/chocolate-cold-coffee.png', 'Rich blended cold coffee infused with Belgian chocolate fudge and chocolate chips.', False), # Set to False for Out of Stock Demo

        # Salads
        ('Arugula', 5.90, 'Salads', 'images/arugula.jpg', 'Fresh peppery arugula leaves tossed with cherry tomatoes, parmesan, and balsamic vinaigrette.', True),
        ('Spinach', 4.95, 'Salads', 'images/spinach.jpg', 'Baby spinach, toasted walnuts, goat cheese crumbles, and red wine vinaigrette.', True),
        ('Cauliflower', 5.95, 'Salads', 'images/cauliflower.jpg', 'Roasted cauliflower florets, spiced chickpeas, fresh parsley, and tahini dressing.', True),
        ('Avocado', 5.95, 'Salads', 'images/avocado.jpg', 'Sliced avocados, mixed salad greens, cucumber ribbons, and a zesty lemon-herb vinaigrette.', True),
        ('Cucumber', 4.25, 'Salads', 'images/cucumber.jpg', 'Crispy English cucumber slices tossed with dill, sour cream, and red onion.', True),
        ('Lettuce', 2.99, 'Salads', 'images/lettuce.jpg', 'Crisp romaine lettuce with golden garlic croutons and rich creamy Caesar dressing.', True),
        ('Beets', 2.99, 'Salads', 'images/beets.jpg', 'Sweet roasted beets, feta cheese, mixed greens, and a sweet orange glaze.', True),
        ('Carrots', 2.99, 'Salads', 'images/carrots.jpg', 'Shredded carrots, raisins, toasted pumpkin seeds, and ginger-lime dressing.', True),
        ('Mixed', 4.95, 'Salads', 'images/mixed-salad.jpg', 'Seasonal local organic field greens tossed with a light vinaigrette.', True),
        
        # Soups
        ('Cheddar & Broccoli', 4.95, 'Soups', 'images/cheddar-broccoli.jpg', 'Thick, creamy cheddar cheese soup loaded with fresh broccoli florets.', True),
        ('Pumpkin', 4.95, 'Soups', 'images/pumpkin-soup.jpg', 'Smooth, slow-cooked roasted pumpkin soup infused with coconut milk and nutmeg.', True),
        ('Carrots & Celery', 4.95, 'Soups', 'images/carrots-celery.jpg', 'A clear, aromatic vegetable broth filled with tender carrots and celery ribs.', True),
        ('Cream of Potato', 5.25, 'Soups', 'images/cream-potato.jpg', 'Velvety potato puree soup topped with bacon bits, cheddar, and chives.', True),
        ('Butter Squash', 5.25, 'Soups', 'images/butternut.jpg', 'Rich butternut squash soup roasted with garlic, maple syrup, and sage.', True),
        ('Split Pea', 5.25, 'Soups', 'images/split-pea.jpg', 'Traditional slow-cooked green split pea soup with smoked ham hocks.', True),
        ('Clam Chowder', 6.99, 'Soups', 'images/chowder.jpg', 'Classic New England style clam chowder loaded with sweet ocean clams and diced potatoes.', True),
        ('House Special', 6.99, 'Soups', 'images/house-special.jpg', 'Hearty chef special rustic chicken vegetable soup served with warm crusty bread.', True),
        ('Lobster Bisque', 7.99, 'Soups', 'images/lobster-bisque.jpg', 'Rich, smooth French soup made from lobster shells and cream, finished with cognac.', True),
        
        # Desserts
        ('Chocolate Cheesecake', 5.90, 'Desserts', 'images/choc-cheesecake.jpg', 'Rich dark chocolate baked cheesecake on a buttery chocolate cookie crust.', True),
        ('Sticky Toffee Pudding', 4.95, 'Desserts', 'images/sticky-toffee.jpg', 'Moist sponge cake made with finely chopped dates, covered in warm toffee sauce.', True),
        ('Fried Ice Cream', 5.95, 'Desserts', 'images/fried-icecream.jpg', 'A scoop of premium vanilla ice cream coated in crispy cornflakes and deep fried.', True),
        ('Banana Boat Pie', 5.95, 'Desserts', 'images/banana-boat.jpg', 'Sliced fresh bananas in a graham cracker crust, topped with rich vanilla custard.', True),
        ('Strawberry Pudding', 4.25, 'Desserts', 'images/strawberry-pudding.jpg', 'Sweet strawberry gelatin layers set with fresh organic strawberries and whipped cream.', True),
        ('Rum Cake', 2.99, 'Desserts', 'images/rum-cake.jpg', 'Traditional moist golden bundt cake soaked in sweet dark rum syrup.', True),
        ('Nutella Cheesecake', 2.99, 'Desserts', 'images/nutella-cheesecake.jpg', 'Creamy no-bake cheesecake swirled with hazelnut Nutella chocolate spread.', True),
        ('Tiramisu', 2.99, 'Desserts', 'images/tiramisu.jpg', 'Espresso-soaked ladyfingers layered with whipped mascarpone cheese and cocoa powder.', True),
        ('Brownie Gelato', 4.95, 'Desserts', 'images/brownie-gelato.jpg', 'Warm chocolate fudge brownie topped with a scoop of premium Italian vanilla gelato.', True),
    ]
    for item in items:
        # Check if 6 values are present (new format)
        if len(item) == 6:
            name, price, cat, img, desc, avail = item
        else:
            name, price, cat, img = item
            desc = ""
            avail = True
        MenuItem.objects.create(name=name, price=price, category=cat, image_url=img, description=desc, is_available=avail)

def index(request):
    return render(request, 'index.html')

def menu(request):
    populate_menu()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse("Please log in first to order items.", status=401)
        item_id = request.POST.get('item_id')
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            Order.objects.create(user=request.user, item=menu_item)
            return HttpResponse("Added to order!", status=201)
        except MenuItem.DoesNotExist:
            return HttpResponse("Item not found.", status=400)

    # Get items grouped by category
    coffees = MenuItem.objects.filter(category='Coffee')
    # If no 'Coffee' category exists, check 'Hot Beverages' to show in the general menu
    if coffees.count() == 0:
        coffees = MenuItem.objects.filter(category='Hot Beverages')
        
    salads = MenuItem.objects.filter(category='Salads')
    soups = MenuItem.objects.filter(category='Soups')
    desserts = MenuItem.objects.filter(category='Desserts')

    # Get user's order logs
    user_orders = []
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user).select_related('item').order_by('-created_at')

    context = {
        'coffees': coffees,
        'salads': salads,
        'soups': soups,
        'desserts': desserts,
        'user_orders': user_orders,
    }
    return render(request, 'menu.html', context)

def coffee(request):
    populate_menu()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse("Please log in first to order items.", status=401)
        
        action = request.POST.get('action', 'order')
        item_id = request.POST.get('item_id')
        
        if action == 'toggle_availability':
            if not (request.user.is_staff or request.user.is_superuser):
                return HttpResponse("You are not authorized to perform this action.", status=403)
            try:
                menu_item = MenuItem.objects.get(id=item_id)
                menu_item.is_available = not menu_item.is_available
                menu_item.save()
                return HttpResponse("Availability updated successfully!", status=200)
            except MenuItem.DoesNotExist:
                return HttpResponse("Item not found.", status=400)
        
        # Default order action
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            if not menu_item.is_available:
                return HttpResponse("This item is currently out of stock.", status=400)
            Order.objects.create(user=request.user, item=menu_item)
            return HttpResponse("Added to order!", status=201)
        except MenuItem.DoesNotExist:
            return HttpResponse("Item not found.", status=400)

    # Get coffee items
    hot_beverages = MenuItem.objects.filter(category='Hot Beverages')
    cold_beverages = MenuItem.objects.filter(category='Cold Beverages')

    # Get user order logs
    user_orders = []
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user).select_related('item').order_by('-created_at')

    context = {
        'hot_beverages': hot_beverages,
        'cold_beverages': cold_beverages,
        'user_orders': user_orders,
    }
    return render(request, 'coffee.html', context)

def seat_reservation(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        seat_ids = request.POST.getlist('seat_ids')

        if not customer_name or not seat_ids:
            return HttpResponse("Please enter your name and select at least one seat.", status=400)

        # Check if any seat is already taken
        taken_seats = SeatReservation.objects.filter(seat_code__in=seat_ids)
        if taken_seats.exists():
            taken_codes = ", ".join([res.seat_code for res in taken_seats])
            return HttpResponse(f"Seats already taken: {taken_codes}", status=400)

        # Reserve seats
        try:
            for seat_id in seat_ids:
                SeatReservation.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    seat_code=seat_id,
                    customer_name=customer_name
                )
            return HttpResponse("Reservations confirmed!", status=201)
        except Exception as e:
            return HttpResponse(f"Reservation failed: {str(e)}", status=500)

    # Query all active reservations
    taken_seats = SeatReservation.objects.all()
    return render(request, 'seat_reservation.html', {'taken_seats': taken_seats})

def contact(request):
    return render(request, 'contact.html')

def login_signup(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'signup':
            username = request.POST.get('username')
            email = request.POST.get('email')
            fname = request.POST.get('fname')
            phone_number = request.POST.get('phone_number')
            password = request.POST.get('password')
            profile_pic = request.FILES.get('profile_picture')

            if not username or not email or not password:
                messages.error(request, "Username, email, and password are required.")
                return render(request, 'login_signup.html')

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
                return render(request, 'login_signup.html')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return render(request, 'login_signup.html')
            
            # Create user
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = fname
                user.save()

                # Get profile created by signal and populate additional fields
                profile = user.profile
                profile.phone_number = phone_number

                # Save profile picture if uploaded
                if profile_pic:
                    # Clean filename to avoid path traversal
                    filename = os.path.basename(profile_pic.name)
                    safe_filename = f"{username}_{filename}"
                    upload_dir = os.path.join(settings.BASE_DIR, 'static', 'uploads')
                    if not os.path.exists(upload_dir):
                        os.makedirs(upload_dir)
                    
                    upload_path = os.path.join(upload_dir, safe_filename)
                    with open(upload_path, 'wb+') as destination:
                        for chunk in profile_pic.chunks():
                            destination.write(chunk)
                    
                    profile.profile_picture = f"/static/uploads/{safe_filename}"
                
                profile.save()

                messages.success(request, "Registration successful! Please login.")
                return redirect('login_signup')
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
                return render(request, 'login_signup.html')

        elif action == 'login':
            # Support login with either username or email
            login_id = request.POST.get('email')  # input field name is 'email'
            password = request.POST.get('password')

            if not login_id or not password:
                messages.error(request, "Username/Email and password are required.")
                return render(request, 'login_signup.html')

            # Check if login_id is email
            username = login_id
            if '@' in login_id:
                try:
                    user_obj = User.objects.get(email=login_id)
                    username = user_obj.username
                except User.DoesNotExist:
                    pass

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username/email or password.")
                return render(request, 'login_signup.html')

    return render(request, 'login_signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')