#!/usr/bin/env python
import asyncio
import aiohttp
import base64
import logging
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from optparse import OptionParser
import requests
import time

requests.packages.urllib3.disable_warnings()

stdlogger = logging.getLogger(__name__)


def task_img(link, page_url, hdr):
    image_url = urljoin(page_url, link['src'])
    # stdlogger.info("loading image " + image_url)
    image = requests.get(image_url, headers=hdr, verify=False)
    stdlogger.info(str(image.status_code) + ' ' +
                   image.headers['content-type'] +
                   ' ' + image_url)
    encoded = base64.b64encode(image.content)
    link['src'] = "data:image/png;base64," + encoded.decode()
    return link


class Crawler():

    hdr = {'User-Agent': 'Mozilla/5.0'}
    html = ''
    title = ''
    url = ''
    content_type = ''

    def crawl(self, page_url):

        self.url = page_url
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # crawlResult = CrawlResult(page_url)
        tmps1 = time.time()
        loop.run_until_complete(self.convert_url_to_html(page_url))
        tmps2 = time.time() - tmps1
        stdlogger.info("Time crawling %d(s) for %s \n" % (tmps2, page_url))

    def __url_can_be_converted_to_data(self, tag):
        return tag.name.lower() == "img" and \
            tag.has_attr('src') and not re.match('^data:', tag['src'])

    def crawl_title(self, page_url):

        try:
            stdlogger.info("Reading page " + page_url)
            page = requests.get(page_url, headers=self.hdr, verify=False)
            stdlogger.info("Page load complete, processing")
            soup = BeautifulSoup(page.content, "html.parser")

            title = soup.find('title')
            if title is not None:
                self.title = title.text
            else:
                stdlogger.info("No title found!")

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            stdlogger.error("Erreur scrapping url:" + page_url)
            stdlogger.error("Error in crawl_url method, stack %s" % (e))
            stdlogger.error(e, exc_info=True)

    @asyncio.coroutine
    def convert_url_to_html(self, page_url):

        try:
            stdlogger.info("Reading page " + page_url)
            page = requests.get(page_url, headers=self.hdr, verify=False)
            stdlogger.info("Page load complete, processing")
            self.content_type = page.headers['content-type']
            soup = BeautifulSoup(page.content, "html.parser")
            # taks = []
            # convert all images in base64
            conn = aiohttp.TCPConnector(verify_ssl=False)
            session = aiohttp.ClientSession(connector=conn)
            for link in soup.findAll(self.__url_can_be_converted_to_data):
                image_url = urljoin(page_url, link['src'])
                image = yield from session.request('GET', image_url, headers=self.hdr)

                stdlogger.info(str(image.status) + ' ' +
                               image.headers['content-type'] +
                               ' ' + image_url)
                content = yield from image.read()
                encoded = base64.b64encode(content)
                link['src'] = "data:image/png;base64," + encoded.decode()

            # write all external css in one tag <style></style>

            for link in soup.findAll("link"):
                if "stylesheet" in link.get("rel", []):
                    new_style_tag = soup.new_tag("style")

                    if soup.head is not None:
                        soup.head.append(new_style_tag)
                    else:
                        soup.html.append(new_style_tag)
                    css_url = urljoin(page_url, link['href'])
                    css_data = yield from session.get(
                        css_url, headers=self.hdr)

                    content = yield from css_data.read()

                    new_style_tag.string = '/*' + css_url + ' */' + \
                        content.decode()
                    stdlogger.info(str(css_data.status) + ' ' +
                                   css_data.headers['content-type'] +
                                   ' ' + css_url)

            self.html = soup.prettify(formatter="html")

            yield from session.close()

            return self.html

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
        soup.crawl(page_url)
        output_filename = options.output
        if soup.html is not '':
            stdlogger.info("Writing results to " + output_filename)
            with open(output_filename, "w") as file:
                file.write(soup.html)
