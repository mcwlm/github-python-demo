import unittest
import os
import tempfile
from app import app, db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def register(self, username, email, password, confirm_password):
        return self.client.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
        ), follow_redirects=True)
    
    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
    
    def logout(self):
        return self.client.get('/logout', follow_redirects=True)
    
    def test_register_and_login(self):
        # Test registration
        response = self.register('testuser', 'test@example.com', 'password123', 'password123')
        self.assertIn(b'Your account has been created', response.data)
        
        # Test login with correct credentials
        response = self.login('testuser', 'password123')
        self.assertIn(b'Welcome, testuser', response.data)
        
        # Test accessing dashboard after login
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'Your Account Information', response.data)
        
        # Test logout
        response = self.logout()
        self.assertIn(b'Please login', response.data)
        
        # Test accessing dashboard after logout (should redirect to login)
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Login', response.data)
        self.assertNotIn(b'Dashboard', response.data)
    
    def test_invalid_login(self):
        # Test login with incorrect credentials
        response = self.login('nonexistent', 'wrongpassword')
        self.assertIn(b'Login Unsuccessful', response.data)

if __name__ == '__main__':
    unittest.main()