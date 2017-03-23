#!/usr/bin/env python
import base64
import logging
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from optparse import OptionParser
import requests

stdlogger = logging.getLogger(__name__)


class CrawlData():
    title = ''
    url = ''
    html = ''

    def __init__(self, url):
        self.url = url


class Crawler():

    hdr = {'User-Agent': 'Mozilla/5.0'}

    def crawl(self, page_url):
        crawlData = CrawlData(page_url)
        crawlData.html = self.convert_url_to_html(page_url)
        return crawlData

    def __url_can_be_converted_to_data(self, tag):
        return tag.name.lower() == "img" and \
            tag.has_attr('src') and not re.match('^data:', tag['src'])

    def crawl_title(self, page_url):
        crawlData = CrawlData(page_url)

        try:
            stdlogger.info("Reading page " + page_url)
            page = requests.get(page_url, headers=self.hdr)
            stdlogger.info("Page load complete, processing")
            soup = BeautifulSoup(page.content, "html.parser")

            title = soup.find('title')
            if title is not None:
                crawlData.title = title.text
            else:
                stdlogger.info("No title found!")

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            stdlogger.error("Erreur scrapping url:" + page_url)
            stdlogger.error("Error in crawl_url method, stack %s" % (e))
            stdlogger.error(e, exc_info=True)

        return crawlData

    def convert_url_to_html(self, page_url):

        try:
            stdlogger.info("Reading page " + page_url)
            page = requests.get(page_url, headers=self.hdr)
            stdlogger.info("Page load complete, processing")
            soup = BeautifulSoup(page.content, "html.parser")

            for link in soup.findAll(self.__url_can_be_converted_to_data):
                image_url = urljoin(page_url, link['src'])
                stdlogger.info("loading image " + image_url)
                image = requests.get(image_url, headers=self.hdr)

                encoded = base64.b64encode(image.content)
                link['src'] = "data:image/png;base64," + encoded.decode()

                new_style_tag = soup.new_tag("style")
                soup.head.append(new_style_tag)
                for link in soup.findAll("link"):
                    if "stylesheet" in link.get("rel", []):
                        css_url = urljoin(page_url, link['href'])
                        css_data = requests.get(css_url, headers=self.hdr)
                        new_style_tag.string = css_data.content.decode()
                        stdlogger.info(css_url)

            html = soup.prettify(formatter="html")
            return html

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            stdlogger.error("Erreur scrapping url:" + page_url)
            stdlogger.error(
                "Error in convert_url_to_html method, stack %s" % (e))
            stdlogger.error(e, exc_info=True)

        return ''


if __name__ == "__main__":
    usage = "usage: %prog http://www.server.com/page.html"
    parser = OptionParser(usage=usage,
                          description="Convert all external images to data urls")
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="debug",
                      help="Turn on debug logging, prints base64 encoded images")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
                      help="turn off all logging")
    parser.add_option("-o", "--output", action="store", dest="output",
                      default="output.html",
                      help="output file name, defaults to output.html")
    (options, args) = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if options.debug else
                        (logging.ERROR if options.quiet else logging.INFO))

    for page_url in args:
        soup = Crawler()
        html = soup.convert_url_to_html(page_url)
        output_filename = options.output
        stdlogger.info("Writing results to " + output_filename)
        with open(output_filename, "w") as file:
            file.write(html)
