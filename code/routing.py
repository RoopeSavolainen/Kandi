import win32com.client as com
import numpy
import scipy.sparse

from settings import *
from main import print_status
import datacollector

class Pathfinder:
    dists = numpy.ndarray([0,0])
    congestion = numpy.ndarray([0,0])

    main_links = []
    connectors = []

    connections = {}
    connections_rev = {}
    link_indices = {}

    use_congestion = False

    goals = []
    routes = numpy.ndarray([0,0])

    data = None

    def __init__(self, vissim, data, process=True):
        self.vissim = vissim
        self.data = data

        links = self.vissim.Net.Links.GetAll()
        self.main_links = filter(lambda c: int(c.AttValue('IsConn')) == 0, links)
        self.connectors = filter(lambda c: int(c.AttValue('IsConn')) == 1, links)
        self.goals = filter(lambda l: l.AttValue('Goal') != 0, self.main_links)

        for i in range(len(self.main_links)):
            no = self.main_links[i].AttValue('No')
            self.link_indices[no] = i

        for i in range(len(self.connectors)):
            connector = self.connectors[i]
            src = int(connector.AttValue('FromLink'))
            dst = int(connector.AttValue('ToLink'))
            self.connections[i] = (src, dst)

            src_i = self._get_link_index(src)
            dst_i = self._get_link_index(dst)
            self.connections_rev[(src_i, dst_i)] = i

        size = len(self.main_links)
        self.weights = numpy.zeros([size, size])
        self.congestion = numpy.full([size, size], 1.0)

        print_status('Pathfinding structures created (%d link segments)' % len(self.main_links))

        if process:
            self._init_routes()

        self.calculate_distances()

        if process:
            print_status('Creating data measurement points')
            self.data.create_measurement_points(self.connectors)


    def calculate_distances(self):
        print_status('= Calculating link distances')
        for i in range(len(self.connectors)):
            src = self.connections[i][0]
            dst = self.connections[i][1]

            conn = self.connectors[i]
            length = float(self._get_link(src).AttValue('Length2D')) + float(conn.AttValue('Length2D'))
            self.weights[self._get_link_index(dst), self._get_link_index(src)] = length


    def update_congestion(self):
        print_status('= Calculating congestion values')
        for i in range(len(self.connectors)):
            src = self.connections[i][0]
            dst = self.connections[i][1]

            coeff = self._get_link_congestion(i)
            self.congestion[self._get_link_index(dst), self._get_link_index(src)] = coeff


    def update_routes(self, force_new=False):
        w = self.weights * self.congestion
        goal_indices = map(lambda g: self._get_link_index(g.AttValue('No')), self.goals)

        print_status('= Calculating Dijkstra')
        _, self.routes = scipy.sparse.csgraph.dijkstra(w, directed=True, return_predecessors=True, indices=goal_indices)

        print_status('= Updating routes')
        for dec in self.vissim.Net.VehicleRoutingDecisionsStatic:
            src = self._get_link_index(dec.Link.AttValue('No'))
            for i in range(dec.VehRoutSta.Count):
                route = dec.VehRoutSta.ItemByKey(i+1)

                dst = self._get_link_index(route.DestLink.AttValue('No'))
                dst_link = self.main_links[dst]
                dst_pos = dst_link.AttValue('Length2D') - 0.1

                newroute = []
                newroute.append(self.main_links[src])
                newroute.append(0.1)
                via = src
                while via != dst:
                    next_index = self.routes[i, via]
                    next_link = self.main_links[next_index]

                    conn_index = self.connections_rev[(via, next_index)]
                    conn = self.connectors[conn_index]

                    newroute.append(conn)
                    newroute.append(0.1)

                    newroute.append(next_link)
                    newroute.append(0.1)

                    via = next_index

                newroute.append(dst_link)
                newroute.append(dst_pos)

                #dec.VehRoutSta.RemoveVehicleRouteStatic()


    def _init_routes(self):
        print_status('= Generating initial routes')
        for veh_in in self.vissim.Net.VehicleInputs:
            link_in = veh_in.Link
            i = veh_in.AttValue('No')

            decisions = self.vissim.Net.VehicleRoutingDecisionsStatic
            dec = decisions.AddVehicleRoutingDecisionStatic(i, link_in, 0.1)

            for goal in self.goals:
                goal_pos = goal.AttValue('Length2D')

                j = dec.VehRoutSta.Count + 1
                route = dec.VehRoutSta.AddVehicleRouteStatic(j, goal, goal_pos - 0.1)


    def _get_link_congestion(self, n):
        flw = self.data.get_flow(n+1)
        return 1.0 + flw * PATHFINDING_PERIOD # TODO: check this


    def _get_link(self, n):
        index = self._get_link_index(n)
        return self.main_links[index]

    def _get_link_index(self, n):  # Mapping from Link.No to python index
        return self.link_indices[n]
