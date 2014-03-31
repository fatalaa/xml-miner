__author__ = 'tmolnar'

import ConfigParser
import os
import requests
from xml.dom import minidom

class Provider(object):

    #PROPERTY_FILE_NAME = 'defaultProviders.properties'
    #PROPERTY_FILE_WITH_PATH = (os.path.dirname(os.path.realpath(__file__)) + os.sep + PROPERTY_FILE_NAME).replace('\\', '/')

    def __init__(self):
        self.name = str()
        self.url = str()
        self.providerInfoIndex = int()
        self.row = int()
        self.depth = int()

    def __str__(self):
        return str.format('Name: %s url: %s', self.name, self.url)

    def get_category_xml(self):
        raise NotImplementedError

    def process(self, depth, node, sheet, col, providerInfoIndex):
        raise NotImplementedError

    def tabulate(self, depth):
        tab = str()
        for i in xrange(0, 4):
            tab += "----"
        return tab

class ShoppingDotComProvider(Provider):
    def __init__(self):
        super(ShoppingDotComProvider, self).__init__()
        self.name = 'Shopping.com'
        self.url = 'http://sandbox.api.ebaycommercenetwork.com/publisher/3.0/rest/CategoryTree?apiKey=78b0db8a-0ee1-4939-a2f9-d3cd95ec0fcc&visitorUserAgent&visitorIPAddress&trackingId=7000610&categoryId=0&showAllDescendants=true'
        self.providerInfoIndex = 0


    def get_category_xml(self):
        response = requests.get(self.url)
        return minidom.parseString(response.content)

    def process(self, depth, node, sheet, col, providerInfoIndex):
        children = node.childNodes
        if len(children) <= 0 and node.nodeName == 'name':
            #print self.tabulate(depth) + str(node.nodeValue)
            sheet.write(self.row, col, node.nodeValue)
            self.row += 1
        else:
            if node.nodeName == 'category':
                col += 1
            for child in children:
                if child.nodeName == 'category':
                    if len(child.childNodes[0].childNodes) > 0:
                        nameElementValue = child.childNodes[0].childNodes[0].nodeValue
                        #print self.tabulate(depth) + str(nameElementValue)
                        sheet.write(self.row, col, nameElementValue)
                        self.row += 1
                self.process(depth + 1, child, sheet, col, 1)



class EbayProvider(Provider):
    def get_root_category_xml(self):
        response = requests.get(self.url)
        return minidom.parseString(response.content)


class WalMartProvider(Provider):
    def __init__(self):
        super(WalMartProvider, self).__init__()
        self.name = 'Walmart.com'
        self.url = 'http://api.walmartlabs.com/v1/taxonomy?apiKey=mgdmgwbhhku48fuz3yhq5g77&format=xml'
        self.providerInfoIndex = 1

    def get_category_xml(self):
        response = requests.get(self.url)
        return minidom.parseString(response.content.strip())


    def process(self, depth, node, sheet, col, providerInfoIndex):
        children = node.childNodes
        if len(children) == 1 and node.nodeName == u'name':
            sheet.write(self.row, col, node.childNodes[0].nodeValue)
            #print self.tabulate(depth) + str(node.childNodes[0].nodeValue)
            self.row += 1
        else:
            if node.nodeName == 'category':
                col += 1
            for child in children:
                self.process(depth + 1, child, sheet, col, 1)


#class MacysProvider(Provider):