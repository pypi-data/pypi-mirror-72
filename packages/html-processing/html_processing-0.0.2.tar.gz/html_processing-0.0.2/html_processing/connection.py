import requests
from lxml import etree
from lxml.html import HtmlElement

from html_processing.parser import get_html_parser


def lxml_connect(url):
    """
    Connects to URL and returns the HTML Tree
    :param url: The URL to the target data source
    :type url: str
    :return: a Subclass of etree.ElementBase, dependent on what is specified in the parser
    :rtype: HtmlElement
    """
    parser = get_html_parser()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'
    headers = {'User-Agent': user_agent}
    res = requests.get(url, headers=headers)

    html_tree: HtmlElement = etree.fromstring(res.content, parser=parser)
    return html_tree
