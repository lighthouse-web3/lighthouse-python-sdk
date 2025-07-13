import unittest
from src.lighthouseweb3 import Lighthouse


class TestCreateWallet(unittest.TestCase):

    async def test_get_access_condition(self):
        """test static create wallet function"""
        cid = 'QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH'
        res = await Lighthouse.getAccessCondition(cid=cid)
        self.assertIsInstance(res, dict)
        self.assertEqual(res.get("data").get("cid"), cid)
