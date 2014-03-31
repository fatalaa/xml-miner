from xmlminer.providers.provider import Provider, ShoppingDotComProvider

__author__ = 'Tibor'
import unittest

class ProviderTest(unittest.TestCase):
    def testValueOf(self):
        provider = Provider.value_of('Shopping.com')
        self.assertTrue(provider is not None)

    def testValueOf2(self):
        provider = ShoppingDotComProvider()
        self.assertTrue(provider is not None)
        dom = provider.get_category_xml()
        self.assertTrue(dom is not None)


if __name__ == '__main__':
    unittest.main()