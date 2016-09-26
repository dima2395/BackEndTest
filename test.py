import bleach
from urllib.parse import urlparse

def filter_src(name, value):
  if name == 'src':
    url = urlparse(value)
    if url.netloc in ['youtube.com', 'play.md', 'vimeo.com']:
      return True

tags = ['p','a','b','i','strong','em', 'img','iframe']
attrs = {
  '*': ['class'],
  'a': ['href'],
  'img': ['src'],
  'iframe': filter_src
}

print(bleach.clean('<iframe src="https://youtube.com/asd/dsa"></iframe>', tags=tags, attributes=attrs))
