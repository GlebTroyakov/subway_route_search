class Vertex:
    def __init__(self):
        self._links = []  # example of Link

    @property
    def links(self):
        return self._links

    def get_link(self, link):
        if link not in self._links:
            self._links.append(link)


class Link:
    pass


class LinkedGraph:
    pass

