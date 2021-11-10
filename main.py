import smbus
import time
from INA260_MINIMAL import INA260

DEVICE_BUS = 1
DEVICE_ADDR = 0x40

def main():
	ina260 = INA260(DEVICE_ADDR)
	ina260.reset_chip()

if __name__ == '__main__':  
   main()


