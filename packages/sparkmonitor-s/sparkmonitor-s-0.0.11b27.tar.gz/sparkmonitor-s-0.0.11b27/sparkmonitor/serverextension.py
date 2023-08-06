"""SparkMonitor Jupyter Web Server Extension

This module adds a custom request handler to Jupyter web server.
It proxies the Spark Web UI by default running at 127.0.0.1:4040
to the endpoint notebook_base_url/sparkmonitor

TODO Create unique endpoints for different kernels or spark applications.
"""

from notebook.base.handlers import IPythonHandler
import tornado.web
from tornado import httpclient
import json
import re
import os
from bs4 import BeautifulSoup
import asyncio
from pyspark import SparkContext
import logging

global logger
logger = logging.getLogger("sparkmonitorUI")
logger.setLevel(logging.DEBUG)
logger.propagate = False
# For debugging this module - Writes logs to a file
fh = logging.FileHandler("sparkmonitor_UI.log", mode="w")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(levelname)s:  %(asctime)s - %(name)s - %(process)d - %(processName)s - \
    %(thread)d - %(threadName)s\n %(message)s \n")
fh.setFormatter(formatter)
logger.addHandler(fh)

proxy_root = "/sparkmonitor"
proxy_root2 = '/sparkmonitor2'

class SparkMonitorHandler2(IPythonHandler):
    """A custom tornado request handler to proxy Spark Web UI requests."""
 

    async def get(self):
        """Handles get requests to the Spark UI

        Fetches the Spark Web UI from the configured ports
        """
        # print("SPARKMONITOR_SERVER: Handler GET")
        baseurl = os.environ.get("SPARKMONITOR_UI_HOST", "127.0.0.1")
        port = os.environ.get("SPARKMONITOR_UI_PORT", "4041")
        logger.info('CURRENT PORT:' + str(port))
        url = "http://" + baseurl + ":" + port
        logger.info("SPARKMONITOR_SERVER: Request URI" + self.request.uri)
        logger.info("SPARKMONITOR_SERVER: Getting from " + url)
        request_path = self.request.uri[(
            self.request.uri.index(proxy_root2) + len(proxy_root2) + 1):] 
        self.replace_path = self.request.uri[:self.request.uri.index(
            proxy_root2) + len(proxy_root2)]
        logger.info("SPARKMONITOR_SERVER: Request_path " + request_path + " \n Replace_path:" + self.replace_path)
        backendurl = url_path_join(url, request_path)
        self.debug_url = url
        self.backendurl = backendurl
        logger.info('REQUEST URI: '+ self.request.uri)
        logger.info("DEBUG_URL: " + self.debug_url)
        logger.info("BACKEND_URL: " + self.backendurl)
        http = httpclient.AsyncHTTPClient()
        try:
            response = await http.fetch(backendurl)
            # response = await http.fetch(SparkContext._active_spark_context.uiWebUrl)
        except Exception as e:
            logger.error("SPARKMONITOR_SERVER: Spark UI Error ",e)
        else:
            self.handle_response(response)

    def handle_response(self, response):
        """Sends the fetched page as response to the GET request"""
        if response.error:
            content_type = "application/json"
            content = json.dumps({"error": "SPARK_UI_NOT_RUNNING",
                                  "url": self.debug_url, "backendurl": self.backendurl, "replace_path": self.replace_path})
            logger.error("SPARKMONITOR_SERVER: Spark UI not running")
        else:
            content_type = response.headers["Content-Type"]
            # print("SPARKSERVER: CONTENT TYPE: "+ content_type + "\n")
            if "text/html" in content_type:
                content = replace(response.body, self.replace_path)
            elif "javascript" in content_type:
                body="location.origin +'" + self.replace_path + "' "
                content = response.body.replace(b"location.origin",body.encode())
            else:
                # Probably binary response, send it directly.
                content = response.body
        self.set_header("Content-Type", content_type)
        self.write(content)
        self.finish()
    

class SparkMonitorHandler(IPythonHandler):
    """A custom tornado request handler to proxy Spark Web UI requests."""
 

    async def get(self):
        """Handles get requests to the Spark UI

        Fetches the Spark Web UI from the configured ports
        """
        # print("SPARKMONITOR_SERVER: Handler GET")
        baseurl = os.environ.get("SPARKMONITOR_UI_HOST", "127.0.0.1")
        port = os.environ.get("SPARKMONITOR_UI_PORT", "4040")
        logger.info('CURRENT PORT:' + str(port))
        global proxy_root
        url = "http://" + baseurl + ":" + port
        logger.info("SPARKMONITOR_SERVER: Request URI" + self.request.uri)
        logger.info("SPARKMONITOR_SERVER: Getting from " + url)
        request_path = self.request.uri[(
            self.request.uri.index(proxy_root) + len(proxy_root) + 1):] + proxy_sub
        self.replace_path = self.request.uri[:self.request.uri.index(
            proxy_root) + len(proxy_root)]
        logger.info("SPARKMONITOR_SERVER: Request_path " + request_path + " \n Replace_path:" + self.replace_path)
        backendurl = url_path_join(url, request_path)
        self.debug_url = url
        self.backendurl = backendurl
        logger.info('REQUEST URI: '+ self.request.uri)
        logger.info("DEBUG_URL: " + self.debug_url)
        logger.info("BACKEND_URL: " + self.backendurl)
        http = httpclient.AsyncHTTPClient()
        try:
            response = await http.fetch(backendurl)
            # response = await http.fetch(SparkContext._active_spark_context.uiWebUrl)
        except Exception as e:
            logger.error("SPARKMONITOR_SERVER: Spark UI Error ",e)
        else:
            self.handle_response(response)

    def handle_response(self, response):
        """Sends the fetched page as response to the GET request"""
        if response.error:
            content_type = "application/json"
            content = json.dumps({"error": "SPARK_UI_NOT_RUNNING",
                                  "url": self.debug_url, "backendurl": self.backendurl, "replace_path": self.replace_path})
            logger.error("SPARKMONITOR_SERVER: Spark UI not running")
        else:
            content_type = response.headers["Content-Type"]
            # print("SPARKSERVER: CONTENT TYPE: "+ content_type + "\n")
            if "text/html" in content_type:
                content = replace(response.body, self.replace_path)
            elif "javascript" in content_type:
                body="location.origin +'" + self.replace_path + "' "
                content = response.body.replace(b"location.origin",body.encode())
            else:
                # Probably binary response, send it directly.
                content = response.body
        self.set_header("Content-Type", content_type)
        self.write(content)
        self.finish()


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the Jupyter server extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    print("SPARKMONITOR_SERVER: Loading Server Extension")
    web_app = nb_server_app.web_app
    host_pattern = ".*$"
    route_pattern = url_path_join(web_app.settings["base_url"], proxy_root + "/.*")
    route_pattern2 = url_path_join(web_app.settings["base_url"], proxy_root2 + "/.*")
    web_app.add_handlers(host_pattern, [(route_pattern, SparkMonitorHandler)])
    web_app.add_handlers(host_pattern, [(route_pattern2, SparkMonitorHandler2)])


try:
    import lxml
except ImportError:
    BEAUTIFULSOUP_BUILDER = "html.parser"
else:
    BEAUTIFULSOUP_BUILDER = "lxml"
# a regular expression to match paths against the Spark on EMR proxy paths
PROXY_PATH_RE = re.compile(r"\/proxy\/application_\d+_\d+\/(.*)")
# a tuple of tuples with tag names and their attribute to automatically fix
PROXY_ATTRIBUTES = (
    (("a", "link"), "href"),
    (("img", "script"), "src"),
)


def replace(content, root_url):
    """Replace all the links with our prefixed handler links,

     e.g.:
    /proxy/application_1467283586194_0015/static/styles.css" or
    /static/styles.css
    with
    /spark/static/styles.css
    """
    soup = BeautifulSoup(content, BEAUTIFULSOUP_BUILDER)
    for tags, attribute in PROXY_ATTRIBUTES:
        for tag in soup.find_all(tags, **{attribute: True}):
            value = tag[attribute]
            match = PROXY_PATH_RE.match(value)
            if match is not None:
                value = match.groups()[0]
            tag[attribute] = url_path_join(root_url, value)
    return str(soup)


def url_path_join(*pieces):
    """Join components of url into a relative url

    Use to prevent double slash when joining subpath. This will leave the
    initial and final / in place
    """
    initial = pieces[0].startswith("/")
    final = pieces[-1].endswith("/")
    stripped = [s.strip("/") for s in pieces]
    result = "/".join(s for s in stripped if s)
    if initial:
        result = "/" + result
    if final:
        result = result + "/"
    if result == "//":
        result = "/"
    return result
