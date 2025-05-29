import unittest
from app import app, users
from flask import url_for

class FlaskLoginTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        self.app_context.pop()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Flask', response.data)
    
    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)
    
    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_successful_login(self):
        # Test login with valid credentials
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)
        self.assertIn(b'Hello, admin', response.data)
    
    def test_failed_login(self):
        # Test login with invalid credentials
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'wrong_password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_profile_page_requires_login(self):
        # Test that profile page redirects to login when not authenticated
        response = self.client.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        self.assertNotIn(b'User Profile', response.data)
    
    def test_logout(self):
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'password'
        }, follow_redirects=True)
        
        # Then test logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)
        self.assertIn(b'Please login', response.data)

if __name__ == '__main__':
    unittest.main()