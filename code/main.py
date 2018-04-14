import win32com.client as com
from settings import *

def main():
    vissim = com.Dispatch(COM_NAME)
    vissim.LoadNet(FILENAME)
    vissim.Simulation.RunContinuous()


if __name__ == '__main__':
    main()
