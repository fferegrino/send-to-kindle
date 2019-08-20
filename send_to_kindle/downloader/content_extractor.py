class ContentExtractor:
    def extract(self, soup):
        return str(soup)


class MediumExtractor(ContentExtractor):
    def extract(self, soup):
        return str(soup.find("article"))
