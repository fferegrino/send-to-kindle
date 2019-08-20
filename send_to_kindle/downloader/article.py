class Article:

    def __init__(self, url, title):
        self.url = url
        self.title = title
        self._content = None
    
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
    
