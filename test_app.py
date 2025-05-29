import unittest
import json
from app import app, db, Appointment

class AppointmentAPITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_get_slots_valid_date(self):
        with app.app_context():
            db.session.add(Appointment(name='Test', phone='123', date='2025-05-30', time_slot='10:00'))
            db.session.commit()

        response = self.client.get('/api/available-slots?date=2025-05-30')
        self.assertEqual(response.status_code, 200)
        slots = json.loads(response.data)
        self.assertNotIn('13:00', slots)  # Break time slot should not appear
        self.assertNotIn('10:00', slots)  # Booked slot should be excluded

    def test_get_slots_no_date_param(self):
        response = self.client.get('/api/available-slots')
        self.assertEqual(response.status_code, 200)
        slots = json.loads(response.data)
        self.assertTrue(len(slots) > 0)  # Should return slots (maybe for None or today)

    def test_get_slots_date_no_bookings(self):
        response = self.client.get('/api/available-slots?date=2025-06-01')  # Date with no bookings
        self.assertEqual(response.status_code, 200)
        slots = json.loads(response.data)
        self.assertIn('10:00', slots)  # All slots should be available

    def test_book_slot_success(self):
        payload = {
            'name': 'Sajad',
            'phone': '9999999999',
            'date': '2025-05-30',
            'time_slot': '10:30'
        }
        response = self.client.post('/api/book', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Appointment booked successfully', response.data)

    def test_book_slot_double_booking(self):
        # First booking
        with app.app_context():
            db.session.add(Appointment(name='Someone', phone='111', date='2025-05-30', time_slot='11:00'))
            db.session.commit()

        # Attempt double booking same slot
        payload = {
            'name': 'Sajad',
            'phone': '222',
            'date': '2025-05-30',
            'time_slot': '11:00'
        }
        response = self.client.post('/api/book', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Slot already booked', response.data)

    def test_book_slot_missing_fields(self):
        payload = {
            'name': 'Sajad',
            # 'phone' missing
            'date': '2025-05-30',
            'time_slot': '12:00'
        }
        response = self.client.post('/api/book', json=payload)
        self.assertIn(response.status_code, [400, 500])

if __name__ == '__main__':
    unittest.main()