import matplotlib.pyplot as plt
import json
from settings import *

class Figures:
    directory = None
    
    def __init__(self, directory):
        self.directory = directory


    def generate_graphs(self):
        f = open(RESULT_FILE, 'r')
        data = json.load(f)
        f.close()

        for key in data:
            flw = [x[0] for x in data[key]]
            spd = [x[1] for x in data[key]]
            dns = [x[2] for x in data[key]]

            basename = self.directory + key.replace(' ', '_')

            plt.scatter(dns, flw)
            plt.xlabel('Density [vehicles/min]')
            plt.ylabel('Flow')
            name = basename + '_flw_dns.png'
            plt.savefig(name)

            plt.scatter(dns, spd)
            plt.xlabel('Density')
            plt.ylabel('Velocity')
            name = basename + '_spd_dns.png'
            plt.savefig(name)


