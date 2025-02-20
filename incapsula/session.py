from __future__ import absolute_import

  <<<<<<< main
import re
import time
  =======
  <<<<<<< dependabot/pip/requests-2.20.0
import re
import time
  =======
  >>>>>>> feature-parsers
  >>>>>>> feature-parsers
import logging
import datetime
import random
from six.moves.urllib.parse import quote, urlsplit

from requests import Session

from .parsers import WebsiteResourceParser, IframeResourceParser
from .errors import RecaptchaBlocked, MaxRetriesExceeded


logger = logging.getLogger('incapsula')

# A list of valid values which are tested in the incapsula test method.
# These values are pulled straight from my browser and should be enough to spoof
# the robot check when setting the cookie.
o = [
    ('navigator', 'true'),
    ('navigator.vendor', 'Google Inc.'),
    ('navigator.appName', 'Netscape'),
    ('navigator.plugins.length==0', 'false'),
    ('navigator.platform', 'Linux x86_64'),
    ('navigator.webdriver', 'undefined'),
    ('plugin_ext', 'no extention'),
    ('plugin_ext', 'so'),
    ('ActiveXObject', 'false'),
    ('webkitURL', 'true'),
    ('_phantom', 'false'),
    ('callPhantom', 'false'),
    ('chrome', 'true'),
    ('yandex', 'false'),
    ('opera', 'false'),
    ('opr', 'false'),
    ('safari', 'false'),
    ('awesomium', 'false'),
    ('puffinDevice', 'false'),
    ('__nightmare', 'false'),
    ('_Selenium_IDE_Recorder', 'false'),
    ('document.__webdriver_script_fn', 'false'),
    ('document.$cdc_asdjflasutopfhvcZLmcfl_', 'false'),
    ('process.version', 'false'),
    ('navigator.cpuClass', 'false'),
    ('navigator.oscpu', 'false'),
    ('navigator.connection', 'false'),
    ('window.outerWidth==0', 'false'),
    ('window.outerHeight==0', 'false'),
    ('window.WebGLRenderingContext', 'true'),
    ('document.documentMode', 'undefined'),
    ('eval.toString().length', '33')
]


def test():
    """
    Quote each value in the tuple list and return a comma delimited string of the parameters.

    This method is a shortened version of incapsulas test method. What the original method does is check
    for specific plugins in your browser and set a cookie based on which extensions you have installed.
    The list of the values is taken from my own browser after running the test method so they are all valid.

    This is just more of a shortcut method instead of trying to reverse engineer the entire code that they had.
    :return:
    """
    # safe param set to () for the single parameter with the key of "eval.toString().length".
    # This is needed to match the cookie value exactly with what is expected from incapsula.
    r = [quote('='.join(x), safe='()') for x in o]
    return ','.join(r)


def simple_digest(s):
    """
    Create a sum of the ordinal values of the characters passed in from s.

    .. code-block: javascript
        // The original javascript code.
        function simpleDigest(mystr) {
            var res = 0;
            for (var i = 0; i < mystr.length; i++) {
                res += mystr.charCodeAt(i);
            }
            return res;
        }

    :param s: The string to calculate the digest from.
    :return: Sum of ordinal values converted to a string.
    """
    res = 0
    for ch in s:
        res += ord(ch)
    return str(res)


class IncapSession(Session):
    """
    Session object to bypass sites which are guarded by incapsula.

    :param max_retries: The number of times to attempt to get the incapsula resource before
        raising a :class:`MaxRetriesExceeded` error. Set this to `None` to never give up.
    :param user_agent: Change the default user agent when sending requests.
    :param cookie_domain: Use this param to change the domain which is set in the cookie.
        Sometimes the domain set for the cookie isn't the same as the actual host.
        i.e. .domain.com instead of www.domain.com.
    :param resource_parser: :class:`ResourceParser` to use when checking whether the website served back a page which
        is blocked by incapsula. Default: :class:`WebsiteResourceParser`.
    :param iframe_parser: :class:`ResourceParser` class (not instance) to use when checking whether the iframe
        contains a captcha. Default: :class:`IframeResourceParser`.
    """

    def __init__(self, max_retries=3, user_agent=None, cookie_domain='', resource_parser=WebsiteResourceParser,
                 iframe_parser=IframeResourceParser):
        super(IncapSession, self).__init__()

        default_useragent = 'IncapUnblockSession (https://github.com/ziplokk1/incapsula-cracker-py3)'
        user_agent = user_agent or default_useragent

        self.max_retries = max_retries
        self.cookie_domain = cookie_domain
        self.headers['User-Agent'] = user_agent

        self.ResourceParser = resource_parser
        self.IframeParser = iframe_parser

    def _get_session_cookies(self):
        """
        Get a list of cookies needed for making the simple digest when setting the ___utvmc cookie.

        .. note:: Translated from:
            function getSessionCookies() {
                var cookieArray = new Array();
                var cName = /^\s?incap_ses_/;
                var c = document.cookie.split(";");
                for (var i = 0; i < c.length; i++) {
                    var key = c[i].substr(0, c[i].indexOf("="));
                    var value = c[i].substr(c[i].indexOf("=") + 1, c[i].length);
                    if (cName.test(key)) {
                        cookieArray[cookieArray.length] = value;
                    }
                }
                return cookieArray;
            }

        :return: List of cookies where the cookie name starts with "incap_ses_".
        """
        return [cookie.value for cookie in self.cookies if cookie.name.startswith('incap_ses_')]

    def _create_cookie(self, name, value, seconds, domain=''):
        """
        Set the incapsula cookie needed to make verification request.

        :param name: Cookie name.
        :param value: Cookie value.
        :param seconds: Cookie expiry seconds from the current time.
        :param domain: Cookie domain.
        :return:
        """
        expires = None
        if seconds:
            d = datetime.datetime.now()
            d += datetime.timedelta(seconds=seconds)
            expires = round((d - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        self.cookies.set(name, value, domain=domain, path='/', expires=expires)

  <<<<<<< main
    def _set_incap_cookie(self, v_array, domain='', sl=None):
  =======
  <<<<<<< dependabot/pip/requests-2.20.0
    def _set_incap_cookie(self, v_array, domain='', sl=None):
  =======
    def _set_incap_cookie(self, v_array, domain=''):
  >>>>>>> feature-parsers
  >>>>>>> feature-parsers
        """
        Calculate the final value for the cookie needed to bypass incapsula.

        .. note:: Translated from:
            function setIncapCookie(vArray) {
                var res;
                try {
                    var cookies = getSessionCookies();
                    var digests = new Array(cookies.length);
                    for (var i = 0; i < cookies.length; i++) {
                        digests[i] = simpleDigest((vArray) + cookies[i]);
                    }
  <<<<<<< main
  =======
  <<<<<<< dependabot/pip/requests-2.20.0
  >>>>>>> feature-parsers
                    var sl = "jcMQV+ffvh2BmAcW8nq2a1HZRZcsB5poBUV2Ew==";
                    var dd = digests.join();
                    var asl = '';
                    for (var i=0;i<sl.length;i++) {
                        asl += (sl.charCodeAt(i) + dd.charCodeAt(i % dd.length)).toString(16);
                    }
                    res = vArray + ",digest=" + dd + ",s=" + asl;
  <<<<<<< main
  =======
  =======
                    res = vArray + ",digest=" + (digests.join());
  >>>>>>> feature-parsers
  >>>>>>> feature-parsers
                } catch (e) {
                    res = vArray + ",digest=" + (encodeURIComponent(e.toString()));
                }
                createCookie("___utmvc", res, 20);
            }

        :param v_array: Comma delimited, urlencoded string which was returned from :func:`simple_digest`.
        :param domain: Cookie domain.
        :return:
        """
        cookies = self._get_session_cookies()
        digests = []
        for cookie_val in cookies:
            digests.append(simple_digest(v_array + cookie_val))
  <<<<<<< main
  =======
  <<<<<<< dependabot/pip/requests-2.20.0
  >>>>>>> feature-parsers

        dd = ','.join(digests)

        asl = self._get_incapsula_asl(dd, sl)

        res = v_array + ',digest=' + dd + ",s=" + asl

  <<<<<<< main
  =======
  =======
        res = v_array + ',digest=' + ','.join(digests)
  >>>>>>> feature-parsers
  >>>>>>> feature-parsers
        logger.debug('setting ___utmvc cookie to {}'.format(res))
        self._create_cookie('___utmvc', res, 20, domain=domain)

    def _raise_for_recaptcha(self, resource):
        """
        Raise an IncapBlocked exception if the iframe contains a recaptcha.

        Send get request to iframe url to get the contents and raise if the contents contain a re-captcha.

        :param resource: Resource object from original request.
        :return:
        """
        # Get the content from the iframe.
        iframe_response = self.get(resource.incapsula_iframe_url, bypass_crack=True)
        iframe_resource = self.IframeParser(iframe_response)

        if iframe_resource.is_blocked():
            raise RecaptchaBlocked(iframe_response, 'resource blocked by re-captcha')

  <<<<<<< main
  =======
  <<<<<<< dependabot/pip/requests-2.20.0
  >>>>>>> feature-parsers
    def _get_incapsula_b(self, incapsula_script_url):
        """
        Get the b var value, which is the obfuscated JS code of incapsula.
        
        :param incapsula_script_url: The url where the b var can be found.
        :return: 
        """
        response = self.get(incapsula_script_url, bypass_crack=True)

        b_search = re.search(r"var b=\"(.*?)\"", response.text)

        if not b_search:
            return None

        return b_search.group(1)

    def _get_incapsula_sl(self, b):
        """
        Get the sl var value from the obfuscated JS code.
        
        .. note:: Code provided by Hades1996 in:
            https://github.com/ziplokk1/incapsula-cracker-py3/issues/4
        
        :param b: Obfuscated JS code where is the sl var value.
        :return: 
        """

        if not b:
            return None

        char_list = []
        for i in range(0, len(b), 2):
            char_list.append(int(b[i:i + 2], base=16))

        code = ""
        for char in char_list:
            code = code + chr(char)

        sl_search = re.search('sl = "(.+)";', code)\

        if sl_search:
            return sl_search.group(1)

        return None

    def _get_incapsula_asl(self, dd, sl):
        """
        Get the asl value to set in the incapsula cookies.
        
        .. note:: Code provided by Hades1996 in:
            https://github.com/ziplokk1/incapsula-cracker-py3/issues/4
        
        :param dd: Digests joined.
        :param sl: SL var value.
        :return: 
        """

        asl = ""
        for i in range(0, len(sl)):
            asl = asl + format(ord(sl[i]) + ord(dd[i % len(dd)]), 'x')
        return asl

    def _apply_cookies(self, original_url, incapsula_script_url):
  <<<<<<< main
  =======
  =======
    def _apply_cookies(self, original_url):
  >>>>>>> feature-parsers
  >>>>>>> feature-parsers
        """
        Set the session cookies and send the necessary GET request to "apply" the cookies.

        :param original_url: The url of the original request.
            Needed to determine the scheme and host of the domain to send the request to apply the cookies.
  <<<<<<< main
  =======
  <<<<<<< dependabot/pip/requests-2.20.0
  >>>>>>> feature-parsers
        :param incapsula_script_url: The url where the b var can be found.
        :return:
        """

  <<<<<<< main
  =======
  =======
        :return:
        """
  >>>>>>> feature-parsers
  >>>>>>> feature-parsers
        # Split the url so that no matter what site is being requested, we can figure out the host of
        # the incapsula resource.
        split = urlsplit(original_url)
        scheme = split.scheme
        host = split.netloc

  <<<<<<< main
  =======
  <<<<<<< dependabot/pip/requests-2.20.0
  >>>>>>> feature-parsers
        b = self._get_incapsula_b(scheme + '://' + host + incapsula_script_url)

        sl = self._get_incapsula_sl(b)

        if sl:
            # Set the cookie then send request to incap resource to "apply" cookie.
            self._set_incap_cookie(test(), self.cookie_domain or host, sl)

            self.get(self.get_incapsula_resource_url(scheme, host), bypass_crack=True)
  <<<<<<< main
  =======
  =======
        # Set the cookie then send request to incap resource to "apply" cookie.
        self._set_incap_cookie(test(), self.cookie_domain or host)
        self.get(self.get_incapsula_resource_url(scheme, host), bypass_crack=True)
  >>>>>>> feature-parsers
  >>>>>>> feature-parsers

    def get_incapsula_resource_url(self, scheme, host):
        """
        Override this method to change the GET request after the cookies are set.

        After the cookies are set, there is a GET request which must get sent to validate the session.
        Override this method to return a different url to send the GET request to.
        This method is more of a future proofing measure than anything.

        :param scheme: 'http' or 'https'.
        :param host: The host of the incapsula resource url. e.x. 'www.example.com'.
        """
        rdm = random.random()
        return scheme + '://' + host + '/_Incapsula_Resource?SWKMTFSR=1&e={}'.format(rdm)

    def crack(self, resp, org=None, tries=0):
        """
        If the response is blocked by incapsula then set the necessary cookies and attempt to bypass it.

        :param resp: Response to check.
        :param org: Original response. Used only when called recursively.
        :param tries: Number of attempts. Used only when called recursively.
        :return:
        """
        # Use to hold the original request so that when attempting the new unblocked request, we have a reference
        # to the original url.
        org = org or resp

        # Return original response after too many tries to bypass incap.
        # If max_retries is None then this part will never get executed allowing a continuous retry.
        if self.max_retries is not None and tries >= self.max_retries:
            raise MaxRetriesExceeded(resp, 'max retries exceeded when attempting to crack incapsula')

        resource = self.ResourceParser(resp)
        if resource.is_blocked():
            logger.debug('Resource is blocked. attempt={} url={}'.format(tries, resp.url))
            # Raise if the response content's iframe contains a recaptcha.
            self._raise_for_recaptcha(resource)

            # Apply cookies and send GET request to apply them.
  <<<<<<< main
            self._apply_cookies(org.url, resource.incapsula_script_url)
  =======
  <<<<<<< dependabot/pip/requests-2.20.0
            self._apply_cookies(org.url, resource.incapsula_script_url)
  =======
            self._apply_cookies(org.url)
  >>>>>>> feature-parsers
  >>>>>>> feature-parsers

            # Recursively call crack() again since if the request isn't blocked after the above cookie-set and request,
            # then it will just return the unblocked resource.
            return self.crack(self.get(org.url, bypass_crack=True), org=org, tries=tries + 1)

        return resp

    def get(self, url, bypass_crack=False, **kwargs):
        """
        Override :class:`Session`.:func:`get`

        :param url: URL for the new :class:`Request` object.
        :param bypass_crack: Use when sending a request that you dont want to go through the incapsula crack.
        :param kwargs: Optional arguments that ``request`` takes.
            Used in this class so when sending a get request from this instance,
            we dont end up creating an infinate loop by calling .get() then .crack() which calls .get()
            and repeat x infinity. Also any requests made to get incapsula resources don't need to be cracked.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)

        # If the request is to get the incapsula resources, then we dont call crack().
        if bypass_crack:
            return self.request('GET', url, **kwargs)

        return self.crack(self.request('GET', url, **kwargs))
