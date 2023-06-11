#!/usr/bin/env python3
import xml.etree.ElementTree as ET
"""
This class parses the descriptions from the RSS-feed, and writes the summaries to them.
"""
class ParseXML:
    """
    Constructor for ParseXML. Takes in a list of summaries and the path to the XML-file.

    Args:
        summaries (list): A list of summaries.
        xml (str): The path to the XML-file.
    """
    def __init__(self, summaries, xml):
        self.summaries = summaries
        self.xml = xml
        self.tree = ET.parse(self.xml)
        self.description = (self.tree.findall('channel/item/description'))

    """
    Edits the descriptions in the XML-file, to instead contain the summaries.
    """
    def __edit_descriptions(self):
        for i in range(len(self.summaries)):
            sentences = self.summaries[i]
            summary = ''
            for j, sentence in enumerate(sentences):
                string = str(sentence).strip('[')
                string = string.strip(']')
                string = string.strip("'")
                string = string.strip ("',")
                if string == ', ':
                    continue
                string = f' {j+1}) ' +string
                string = string + ' \n'
                string = "<br>" + string + "<\\br>"
                summary += string
            self.description[i].text = summary

    """
    Writes the summaries to the XML-file.
    """
    def write(self):
        self.__edit_descriptions()
        self.tree.write(self.xml)
