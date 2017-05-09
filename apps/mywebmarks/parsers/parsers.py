#!/usr/bin/env python
import logging
import sys
from optparse import OptionParser
from html.parser import HTMLParser

stdlogger = logging.getLogger(__name__)


class Folder():
    pass


class MyHTMLParser(HTMLParser):
    tree = {}
    parent = {}
    current = {}

    def handle_starttag(self, tag, attrs):
        if 'dl' == tag:
            print("Encountered a start tag:", tag)
            self.parent = self.current
            self.current = {}

    def handle_endtag(self, tag):
        if 'dl' == tag:
            print("Encountered an end tag :", tag)

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        pass


class FavoriteParser():
    def parse(self, file_name):
        try:
            with open(file_name, "r") as f:
                html_doc = f.read()

            MyHTMLParser().feed(html_doc)

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            stdlogger.error("Erreur parsing file:" + file_name)
            stdlogger.error(
                "Error in convert_url_to_html method, stack %s" % (e))
            stdlogger.error(e, exc_info=True)
        return ''


if __name__ == "__main__":
    usage = "usage: %prog http://www.server.com/page.html"
    parser = OptionParser(usage=usage,
                          description="Parse favori_file")
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="debug",
                      help="Turn on debug logging")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
                      help="turn off all logging")
    parser.add_option("-o", "--output", action="store", dest="output",
                      default="output.html",
                      help="output file name, defaults to output.html")
    (options, args) = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if options.debug else
                        (logging.ERROR if options.quiet else logging.INFO))

    for file_name in args:
        stdlogger.info("Parsing file_name " + file_name)
        parser = FavoriteParser()
        parser.parse(file_name)
