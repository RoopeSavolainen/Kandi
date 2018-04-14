import win32com.client as com
import numpy
import scipy

class Pathfinder:
    dists = numpy.ndarray([0,0])
    congestion = numpy.ndarray([0,0])
    main_links = []
    connectors = []
    link_indices = {}
    use_congestion = False

    def __init__(self, vissim):
        self.vissim = vissim

        links = self.vissim.Net.Links.GetAll()
        self.main_links = filter(lambda c: int(c.AttValue('IsConn')) == 0, links)
        self.connectors = filter(lambda c: int(c.AttValue('IsConn')) == 1, links)

        for i in range(len(self.main_links)):
            no = unicode(self.main_links[i].AttValue('No'))
            self.link_indices[no] = i

        size = len(self.main_links)
        self.weights = numpy.zeros([size, size])
        self.congestion = numpy.zeros([size, size])

        self.calculate_distances()


    def calculate_distances(self):
        for conn in self.connectors:
            src = conn.AttValue('FromLink')
            dst = conn.AttValue('ToLink')

            length = float(self._get_link(src).AttValue('Length2D')) + float(conn.AttValue('Length2D'))
            self.weights[self._get_link_index(dst), self._get_link_index(src)] = length


    def update_congestion(self):
        for conn in self.connectors:
            src = conn.AttValue('FromLink')
            dst = conn.AttValue('ToLink')

            coeff = _get_link_congestion(dst)
            self.congestion[self._get_link_index(dst), self._get_link_index(src)] = coeff


    def _get_link_congestion(self, n):
        link = self._get_link(n)
        return 1.0 # TODO: implement congestion based coefficient


    def _get_link(self, n):
        index = self._get_link_index(n)
        return self.main_links[index]

    def _get_link_index(self, n):
        return self.link_indices[n]
