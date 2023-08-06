from bs4 import BeautifulSoup

class ResponseInterpreter:

    def __init__(self, requestResponse, bs_features="lxml"):
        self.requestResponse = requestResponse
        self.parse_response(features=bs_features)

    def parse_response(self, features="lxml"):
        """
        Takes a request response and parses it using BeautifulSoup module.
        """
        html = self.requestResponse.text
        self.parsed_text = BeautifulSoup(html, features=features)

    def getElementsByType(self, tag, attrs=None):
        """
        isolates a list of html elements

        tag: string
        the tag name, e.g. "p" for a <p> tag
        attrs: dict or string
        attribute values of the target elements, e.g.
        {"href":"http://www.bbc.co.uk"}
        OR
        presence of a specific attribute
        """

        attrs = {attrs:True} if isinstance(attrs,str)\ #Looking for elements which a specific attribute
                    else attrs # Looking for elements with a specific attribute value

        elements = self.parsed_text.findAll(tag, attrs=attrs) if attrs else \
                self.parsed_text.findAll(tag)

        return elements

    def getTextByElementType(self, tag, attrs=None):
        """
        Search for all elements in the soup by the tag and its attributes,
        get element text

        tag: string
        the tag name, e.g. "p" for a <p> tag
        attrs: dict
        attribute values of the target elements, e.g.
        {"href":"http://www.bbc.co.uk"}

        returns: map object of text of searched elements
        """


        elements = self.getElementsByType(tag, attrs=attrs)
        elementsText = map(lambda x: x.text, elements)

        return elementsText

    def getAttributeText(self, tag, target_attr, search_attrs=None):
        """
        Search for all elements in the soup by the tag and its attributes,
        get the text of target_attr back.

        tag: string
        the tag name, e.g. "p" for a <p> tag

        target_attr: string
        the name of the attribute whose text you are looking for

        search_attrs: dict
        attribute values of the target elements, e.g.
        {"href":"http://www.bbc.co.uk"}

        returns: map object of the target attributes
        """

        elements = self.getElementsByType(tag, attrs=search_attrs)
        elementsAttrs = map(lambda x: x[target_attr], elements)

        return elementsAttrs
