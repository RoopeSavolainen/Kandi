import win32com.client as com
import numpy
import scipy

class Pathfinder:
    weights = numpy.ndarray([0,0])
    self.

    def __init__(self, vissim, congestion):
        self.vissim = vissim
        self.update_weights()
        self.congestion = congestion

        links = self.vissim.Net.Links.GetAll()
        self.main_links = filter(lambda c: int(c.AttValue('IsConn')) == 0, links)
        self.connectors = filter(lambda c: int(c.AttValue('IsConn')) == 1, links)

        size = len(self.main_links)
        self.weights = numpy.zeros([size, size])

        self.update_weights()


    def update_weights(self):
       
       for conn in connectors:
           src = int(conn.AttValue('FromLink')) - 1
           dst = int(conn.AttValue('ToLink')) - 1

           length = float(main_links[src].AttValue('Length2D')) + float(conn.AttValue('Length2D'))
           
           if self.congestion:
               coeff = _get_link_congestion(dst)
               length *= coeff

            self.weights[src, dst] = length


    def _get_link_congestion(self, n):
        link = self.main_links[n]
        return 1.0 # TODO: implement congestion based coefficient
