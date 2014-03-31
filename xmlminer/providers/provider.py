__author__ = 'tmolnar'

import ConfigParser
import os
import requests
from xml.dom import minidom

class Provider(object):

    PROPERTY_FILE_NAME = 'defaultProviders.properties'
    PROPERTY_FILE_WITH_PATH = (os.path.dirname(os.path.realpath(__file__)) + os.sep + PROPERTY_FILE_NAME).replace('\\', '/')

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

    @staticmethod
    def value_of(sectionName):
        provider = Provider()
        configParser = ConfigParser.RawConfigParser()
        configParser.read(Provider.PROPERTY_FILE_WITH_PATH)
        provider.name = configParser.get(sectionName, 'name')
        provider.url = configParser.get(sectionName, 'url')
        provider.providerInfoIndex = configParser.getint(sectionName, 'index')
        return provider

class ShoppingDotComProvider(Provider):
    def __init__(self):
        super(ShoppingDotComProvider, self).__init__()
        tmp = Provider.value_of('Shopping.com')
        self.name = tmp.name
        self.url = tmp.url
        self.providerInfoIndex = tmp.providerInfoIndex


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
        tmp = Provider.value_of('Walmart.com')
        self.name = tmp.name
        self.url = tmp.url
        self.providerInfoIndex = tmp.providerInfoIndex

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