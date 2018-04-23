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
            ids = [x[3] for x in data[key]]

            basename = self.directory + key.replace(' ', '_').replace('\xc3\xa4'.decode('iso-8859-1'), 'a')

            plt.scatter(dns, flw)
            plt.xlabel('Density [vehicles/m]')
            plt.ylabel('Flow [vehicles/min]')
            name = basename + '_flw_dns.png'
            plt.savefig(name)
            plt.close()

            plt.scatter(dns, spd)
            plt.xlabel('Density [vehicles/m]')
            plt.ylabel('Velocity [km/h]')
            name = basename + '_spd_dns.png'
            plt.savefig(name)
            plt.close()

            for i in ids:
                flw = [x[0] for x in data[key] if x[3] == i]
                spd = [x[1] for x in data[key] if x[3] == i]
                times = [x[4] for x in data[key] if x[3] == i]

                series = zip(flw, spd, times)
                series = sorted(series, key=lambda x: x[2])

                sets = zip(*series)
                plt.plot(sets[2], sets[0])
                plt.xlabel('Time [s]')
                plt.ylabel('Flow [vehicles/min]')

                name = basename + '_flw_time_' + str(i) + '.png'
                plt.savefig(name)
                plt.close()
                
                plt.plot(sets[2], sets[1])
                plt.xlabel('Time [s]')
                plt.ylabel('Velocity [km/h]')

                name = basename + '_spd_time_' + str(i) + '.png'
                plt.savefig(name)
                plt.close()

