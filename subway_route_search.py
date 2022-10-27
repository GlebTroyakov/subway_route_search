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
    def __init__(self, v1: Vertex, v2: Vertex):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1  # длина связи (по умолчанию 1); это может быть длина пути, время в пути и др.

    def __eq__(self, other):
        assert isinstance(other, Link), 'Сравневается не связь'
        if self._v1 == other._v1 and self._v2 == other._v2:
            return True
        if self._v1 == other._v2 and self._v2 == other._v1:
            return True
        return False

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value


class LinkedGraph:
    pass

