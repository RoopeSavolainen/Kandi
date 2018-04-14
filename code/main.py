import win32com.client as com
import os
from settings import *

def main():
    vissim = com.Dispatch(COM_NAME)
    base_path = os.path.dirname(os.path.abspath(__file__))
    vissim.LoadNet(base_path + FILENAME)
    vissim.Simulation.RunContinuous()


if __name__ == '__main__':
    main()
