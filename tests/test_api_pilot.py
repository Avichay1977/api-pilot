"""Tests for api-pilot."""
import os
import unittest
from api_pilot.resolver import resolve_key
from api_pilot.validators import validate_key

class TestResolver(unittest.TestCase):
    def test_env_resolution(self):
        """Test that ENV variables are resolved first."""
        os.environ['TEST_KEY'] = 'from_env'
        result = resolve_key('TEST_KEY')
        self.assertEqual(result, 'from_env')
        del os.environ['TEST_KEY']
    
    def test_missing_key(self):
        """Test that missing keys return None."""
        result = resolve_key('NONEXISTENT_KEY_12345')
        self.assertIsNone(result)

class TestValidators(unittest.TestCase):
    def test_validator_exists(self):
        """Test that validators are defined."""
        # This will fail with real keys, but tests structure
        success, message = validate_key('nonexistent', 'fake_key')
        self.assertFalse(success)
        self.assertIn('No validator', message)

if __name__ == '__main__':
    unittest.main()
