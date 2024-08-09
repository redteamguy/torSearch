from urllib.parse import urlparse, urlunparse

def validator(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    base_url = urlunparse((scheme, netloc, '', '', '', ''))
    if not base_url.endswith('/'):
        base_url += '/'
        base_url = base_url.split(" ")
    return base_url[0]
# print(validator("hello"))