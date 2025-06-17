import unittest
from app import app, users
from flask import url_for

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = app.test_client()
        
        # Create a test context
        self.app_context = app.test_request_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'Username', response.data)
        self.assertIn(b'Password', response.data)
    
    def test_valid_login(self):
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123',
            'remember': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged in successfully!', response.data)
        self.assertIn(b'You are logged in as', response.data)
    
    def test_invalid_login(self):
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'wrongpassword',
            'remember': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_profile_requires_login(self):
        # Try accessing profile without login
        response = self.client.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Should redirect to login page
        
        # Login and then access profile
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123',
            'remember': False
        })
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Profile', response.data)
        self.assertIn(b'Welcome, admin', response.data)
    
    def test_logout(self):
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123',
            'remember': False
        })
        
        # Then logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)
        
        # Verify we can't access profile after logout
        response = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()