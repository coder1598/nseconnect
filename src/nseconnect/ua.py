import requests
import random
from datetime import datetime as dt
from nseconnect import urls
from time import sleep


class Session():
    __CACHE__ = {}

    def __init__(self, session_refresh_interval=60, cache_timeout=60):
        """Initialize the class instance with session and cache parameters.
        Args:
            session_refresh_interval (int, optional): Time interval in seconds to refresh session. Defaults to 60.
            cache_timeout (int, optional): Cache timeout duration in seconds. Defaults to 20.
        Attributes:
            session_refresh_interval (int): Time interval for session refresh.
            cache_timeout (int): Duration for cache timeout.
        """

        self.session_refresh_interval = session_refresh_interval
        self.cache_timeout = cache_timeout  # cache timeout in seconds
        self._session = None  # Initialize _session attribute to None
        self.create_session()
        self.flush()
    
    def nse_headers(self):
        """Returns a dictionary of headers required for making requests to NSE (National Stock Exchange).
        These headers are designed to mimic a web browser request to prevent request blocking.
        Returns:
            dict: A dictionary containing HTTP headers with the following keys:
                - Accept: Acceptable content types
                - Accept-Language: Preferred language for response
                - user-agent: Browser identification string
                - X-Requested-With: Identifies AJAX requests
        """
        
        return {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.nseindia.com/",
                "Origin": "https://www.nseindia.com",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
                }
    
    def create_session(self):
        """Creates and initializes a new HTTP session for NSE (National Stock Exchange) API requests.
        This method sets up a requests.Session object with appropriate headers for NSE and initializes
        it by making a GET request to the NSE home page. The session is used for subsequent API calls.
        Returns:
            None
        Side Effects:
            - Sets self._session with configured requests.Session object
            - Sets self._session_init_time with current timestamp
        """

        # Clean up old session if it exists
        if hasattr(self, '_session') and self._session is not None:
            old_session = self._session
            self._session = None
            # Explicitly delete old session to ensure garbage collection
            del old_session
            
        # Create a completely new session object
        self._session = requests.Session()
        self._session.headers.update(self.nse_headers())
        
        # First visit NSE home page to get cookies
        self._session.get(urls.NSE_MAIN)
        # Small delay to mimic human behavior
        sleep(1)
        # Visit the market page to get additional cookies
        self._session.get(f"{urls.NSE_MAIN}/market-data/live-equity-market")
        
        self._session_init_time = dt.now()
    
    def flush(self):
        """Flushes the cached user agent data.
        This method clears the internal cache dictionary storing user agent information
        by resetting the class's __CACHE__ attribute to an empty dictionary.
        Returns:
            None
        """
        
        self.__class__.__CACHE__ = {}

    def fetch(self, url):
        """Fetches data from a given URL with caching and session management.
        This method implements a caching mechanism and session refresh logic to optimize 
        network requests. It also includes random delays to prevent rate limiting.
        Args:
            url (str): The URL to fetch data from.
        Returns:
            requests.Response: The response object from the request.
        Note:
            - Uses class-level cache to store responses
            - Implements random delays between 0-300ms before making requests
            - Auto-refreshes session if expired based on session_refresh_interval
        """

        # Check cache first
        if url in self.__class__.__CACHE__:
            cache_time, response = self.__class__.__CACHE__[url]
            if (dt.now() - cache_time).seconds < self.cache_timeout:
                # print("serving from cache")
                return response

        # Only check session expiry if we need to make a network request
        time_diff = dt.now() - self._session_init_time
        if time_diff.seconds >= self.session_refresh_interval:
            # print("re-initing the session because of expiry")
            self.create_session()

        # Add random delay before making request
        sleep_time = random.uniform(0, 0.3)  # Random delay between 0-300ms
        # print(f"Adding random delay of {sleep_time:.3f} seconds")
        sleep(sleep_time)

        # Make actual request if not in cache or cache expired
        try:
            response = self._session.get(url)
            # Force a 401 response to retry with a fresh session
            if response.status_code == 401:
                self.create_session()
                response = self._session.get(url)
        except requests.RequestException:
            # Try again with a fresh session on any request exception
            self.create_session()
            response = self._session.get(url)
            
        self.__class__.__CACHE__[url] = (dt.now(), response)
        return response
