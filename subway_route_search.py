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
    def __init__(self):
        self._links = []  # example of Link
        self._vertex = []  # example of Vertex

    def add_vertex(self, v):
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):
        if link not in self._links:
            self._links.append(link)

        if link._v1 not in self._vertex:
            self._vertex.append(link._v1)

        if link._v2 not in self._vertex:
            self._vertex.append(link._v2)

        link._v1.get_link(link)  # append link in vertex
        link._v2.get_link(link)

    @staticmethod
    def get_link(v, D):
        for i, dist in enumerate(D[v]):
            if dist > 0:
                yield i

    @staticmethod
    def arg_min(T, S):
        amin = -1
        m = max(T)
        for i, t in enumerate(T):
            if t < m and i not in S:
                m = t
                amin = i
        return amin

    def create_d(self):
        inf = float('inf')
        D = []
        for i, v_this in enumerate(self._vertex):
            tmp_dist = []
            for j, v_other in enumerate(self._vertex):  # чтоб потом не транспонировать
                if v_this == v_other:
                    tmp_dist.append(0)
                elif Link(v_this, v_other) in v_this._links:
                    for i in v_this._links:
                        if Link(v_this, v_other) == i:
                            tmp_dist.append(i.dist)
                else:
                    tmp_dist.append(inf)
            D.append(tmp_dist)
        return D

    def find_path(self, start_v, stop_v):
        if start_v not in self._vertex or stop_v not in self._vertex:
            raise ValueError('Одна или обе станции отстутсвуют на карте.')
        else:
            inf = float('inf')
            D = self.create_d()
            v = 0
            N = len(D)
            T = [inf] * N
            S = {v}
            T[v] = 0
            M = [0] * N

            while v != -1:
                for j in self.get_link(v, D):
                    if j not in S:
                        w = T[v] + D[v][j]
                        if w < T[j]:
                            T[j] = w
                            M[j] = v

                v = self.arg_min(T, S)
                if v > 0:
                    S.add(v)

            start = self._vertex.index(start_v)
            end = self._vertex.index(stop_v)
            P = [end]

            while end != start:
                end = M[P[-1]]
                P.append(end)

            if type(start_v) == Vertex:
                lines_path = []
                for i in range(len(P) - 1):
                    for j in self._links:
                        if j == self._links[P[i]]:
                            lines_path.append(j)
                P = P[::-1]
                return (P, lines_path)

            if type(start_v) == Station:
                res_P = [self._vertex[i].name for i in P][::-1]
                lines_path = []
                for i in range(len(res_P) - 1):
                    for j in self._links:
                        if (j.v1.name == res_P[i] and j.v2.name == res_P[i + 1]) or \
                                (j.v2.name == res_P[i] and j.v1.name == res_P[i + 1]):
                            lines_path.append(j)
                return (res_P, lines_path)


class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self._dist = dist


if __name__ == '__main__':
    map1 = LinkedGraph()
    v1 = Vertex()
    v2 = Vertex()
    v3 = Vertex()
    v4 = Vertex()
    map1.add_link(Link(v1, v2))
    map1.add_link(Link(v2, v3))
    map1.add_link(Link(v3, v4))
    map1.add_link(Link(v2, v4))
    assert len(map1._vertex) == 4, 'Неверное число вершин для map1'
    assert len(map1._links) == 4, 'Неверное число связей для map1'
    path_v1_to_v4_map1 = map1.find_path(v1, v4)
    assert path_v1_to_v4_map1[0] == [0, 1, 3], 'Неверный маршрут для невзвешеноого графта для map1'
    assert sum([i.dist for i in path_v1_to_v4_map1[1]]), 'Неверная сумма весов маршрута невзвешенного графта для map1'

    map2 = LinkedGraph()
    v1 = Station(1)
    v2 = Station('2')
    v3 = Station('three')
    v4 = Station('4')
    map2.add_link(LinkMetro(v1, v2, 1))
    map2.add_link(LinkMetro(v2, v3, 2))
    map2.add_link(LinkMetro(v3, v4, 3))
    map2.add_link(LinkMetro(v2, v4, 6))
    assert len(map2._vertex) == 4, 'Неверное число вершин для map2'
    assert len(map2._links) == 4, 'Неверное число связей для map2'
    path_v1_to_v4_map2 = map2.find_path(v1, v4)
    assert path_v1_to_v4_map2[0] == [1, '2', 'three', '4'], 'Неверный маршрут для невзвешеноого графта для map2'
    assert sum([i.dist for i in path_v1_to_v4_map2[1]]) == 6, 'Неверная сумма весов маршрута невзвешенного графта для map2'
    path_v2_to_v4_map2 = map2.find_path(v2, v4)  # проверка из другой точки
    assert path_v2_to_v4_map2[0] == ['2', 'three', '4'], 'Неверный маршрут для невзвешеноого графта для map2'
    assert sum([i.dist for i in path_v2_to_v4_map2[1]]) == 5, 'Неверная сумма весов маршрута невзвешенного графта для map2'
