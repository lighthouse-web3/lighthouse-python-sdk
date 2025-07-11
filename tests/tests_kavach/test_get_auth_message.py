import unittest
import logging
from src.lighthouseweb3 import Kavach

logger = logging.getLogger(__name__)

class TestGetAuthMessage(unittest.IsolatedAsyncioTestCase):
    """Test cases for the getAuthMessage function."""

    async def test_get_auth_message_valid_address(self):
        """Test getting auth message with a valid address."""
        address = 'h6gar47c9GxYda8Kkg5J9So3R9K3jhcWKbgrjKhqfst'
        auth_message = await Kavach.getAuthMessage(address=address)
        
        self.assertIn(
            "Please sign this message to prove you are owner of this account",
            auth_message['message'],
            "Should return a valid auth message"
        )
        self.assertIsNone(auth_message['error'])

    async def test_get_auth_message_invalid_address(self):
        """Test getting auth message with an invalid address."""
        auth_message = await Kavach.getAuthMessage(address="0x9a40b8EE3B8Fe7eB621cd142a651560Fa7")
        
        self.assertIsNone(auth_message['message'])
        self.assertIsNotNone(auth_message['error'])
        self.assertIn("invalid address", str(auth_message["error"]).lower())

if __name__ == '__main__':
    unittest.main(verbosity=2)