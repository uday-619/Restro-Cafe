from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from Myapp.models import MenuItem, Order
from Myapp.views import populate_menu

class CoffeeMenuTestCase(TestCase):
    def setUp(self):
        # Seed the database
        populate_menu()
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        # Create a staff user (owner)
        self.staff_user = User.objects.create_user(username='staffuser', email='staff@example.com', password='password123', is_staff=True)
        self.client = Client()

    def test_coffee_page_get(self):
        response = self.client.get(reverse('coffee'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "la cafe'")
        self.assertContains(response, "Espresso")
        self.assertContains(response, "Cold Brew")

    def test_order_unauthenticated(self):
        # Order a hot beverage (Espresso is typically the first item, let's grab one)
        item = MenuItem.objects.filter(category='Hot Beverages', is_available=True).first()
        response = self.client.post(reverse('coffee'), {'item_id': item.id})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_authenticated_success(self):
        self.client.login(username='testuser', password='password123')
        item = MenuItem.objects.filter(category='Hot Beverages', is_available=True).first()
        response = self.client.post(reverse('coffee'), {'item_id': item.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        
        # Verify order details
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.item, item)

    def test_order_out_of_stock(self):
        self.client.login(username='testuser', password='password123')
        # Seed or find an out of stock item (Chocolate Cold Coffee is marked False)
        item = MenuItem.objects.filter(is_available=False).first()
        self.assertIsNotNone(item, "Should find at least one out of stock item")
        
        response = self.client.post(reverse('coffee'), {'item_id': item.id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_nonexistent_item(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('coffee'), {'item_id': 9999})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_toggle_availability_unauthenticated(self):
        item = MenuItem.objects.first()
        response = self.client.post(reverse('coffee'), {
            'item_id': item.id,
            'action': 'toggle_availability'
        })
        self.assertEqual(response.status_code, 401)

    def test_toggle_availability_non_staff(self):
        self.client.login(username='testuser', password='password123')
        item = MenuItem.objects.first()
        response = self.client.post(reverse('coffee'), {
            'item_id': item.id,
            'action': 'toggle_availability'
        })
        self.assertEqual(response.status_code, 403)

    def test_toggle_availability_staff_success(self):
        self.client.login(username='staffuser', password='password123')
        item = MenuItem.objects.first()
        initial_availability = item.is_available
        
        response = self.client.post(reverse('coffee'), {
            'item_id': item.id,
            'action': 'toggle_availability'
        })
        self.assertEqual(response.status_code, 200)
        
        # Verify the database updated
        item.refresh_from_db()
        self.assertEqual(item.is_available, not initial_availability)


