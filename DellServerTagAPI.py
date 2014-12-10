#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Administrator
#
# Created:     18/08/2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import requests
import json


class TableFormatHasChanged(Exception):
    """The Headers do not match the exepcted format: Part, Qty, Description"""
    pass


def dell_components_from_source_tag(tag, section = "subSectionB"):
    """Simple Script to extract the components associated with the Source Tag for a Dell Server"""


    dell_product_config_url = "http://www.dell.com/support/home/us/en/19/product-support/servicetag/%s/configuration"

    print "Getting Site for %s"%tag
    req = requests.get(dell_product_config_url%tag)
    print "Exracting Data from Beautiful Soup..."
    soup = BeautifulSoup(req.text)

    dell_components_table = soup.find(id = section).table

    output = {'tag': tag, 'components' : []}

    for idx,td in enumerate(dell_components_table.find_all('td')):
        row = []
        for div in td.find_all('div'):
            row.append(div.text.strip())

        if idx ==0 and row != ['Part Number', 'Quantity', 'Description']:
            raise TableFormatHasChanged, "Headers(Part Number, Quantity, Description) aren't recognized"
        else:
            component_dict = {}
            component_dict['part_num'] = row[0]
            component_dict['qty'] = row[1]
            component_dict['description'] = row[2]
            try:
                component_dict['type'] = row[2][:row[2].index(",")]
            except ValueError:
                component_dict['type'] = "UNKNOWN"

            output['components'].append(component_dict)

    return json.dumps(output)




if __name__ == "__main__":
    print dell_components_from_source_tag('ABCDEF1')