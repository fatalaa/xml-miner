__author__ = 'Tibor'
import xlwt
from xmlminer.providers.provider import ShoppingDotComProvider, WalMartProvider
from fitsheetwrapper import FitSheetWrapper


class Exporter():
    def __init__(self):
        self.providers = self.init_providers()
        self.workbook = xlwt.Workbook()

    def init_providers(self):
        li = list(tuple())
        li.append(('Shopping.com', ShoppingDotComProvider()))
        li.append(('Walmart.com', WalMartProvider()))
        return li

    def export(self):
        for provider in self.providers:
            root = provider[1].get_category_xml()
            sheet = FitSheetWrapper(self.workbook.add_sheet(provider[1].name))
            provider[1].row = 0
            provider[1].process(0, root, sheet, 0, provider[1].providerInfoIndex)
            self.workbook.save('categories.xls')