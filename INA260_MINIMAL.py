import smbus
#source: https://github.com/charkster/INA260/tree/077521eded5c8efe22bf843dfd2fa462e10bb9c5
class INA260:
	
	_INA260_DEFAULT_DEVICE_ADDRESS   = 0x40
	_INA260_CONFIG_ADDR      = 0x00
	_INA260_CURRENT_ADDR     = 0x01
	_INA260_BUS_VOLTAGE_ADDR = 0x02
	_INA260_BUS_VOLTAGE_LSB  = 1.25 #mV
	_INA260_CURRENT_LSB      = 1.25 #mA
	
		# Constructor
	def __init__(self, dev_address=_INA260_DEFAULT_DEVICE_ADDRESS):
		self.i2c = smbus.SMBus(1) #/dev/i2c-1
		self.dev_address = dev_address
	
	def twos_compliment_to_int(self, val, len):
		# Convert twos compliment to integer
		if(val & (1 << len - 1)):
			val = val - (1<<len)
		return val
		
	def get_bus_voltage(self):
		raw_read = self.i2c.read_i2c_block_data(self.dev_address,self._INA260_BUS_VOLTAGE_ADDR,2)
		word_rdata = raw_read[0] *256 + raw_read[1]
		vbus = float(word_rdata) / 1000.0 * self._INA260_BUS_VOLTAGE_LSB
		return vbus

	def get_current(self):
		raw_read = self.i2c.read_i2c_block_data(self.dev_address,self._INA260_CURRENT_ADDR,2)
		word_rdata = raw_read[0] *256 + raw_read[1]
		current_twos_compliment = word_rdata
		current_sign_bit = current_twos_compliment >> 15
		if (current_sign_bit == 1):
			current = float(self.twos_compliment_to_int(current_twos_compliment, 16)) / 1000.0 * self._INA260_CURRENT_LSB
		else:
			current = float(current_twos_compliment) / 1000.0 * self._INA260_CURRENT_LSB
		return current

	def reset_chip(self):
		byte_list = [0x80, 0x00]
		self.i2c.write_i2c_block_data(self.dev_address,self._INA260_CONFIG_ADDR,byte_list)
	
	def read_configuration_register(self):
		return self.i2c.read_i2c_block_data(self.dev_address, self._INA260_CONFIG_ADDR, 2)

	def activate_average(self, samples): 
		byte_list = [0x61, 0x27]
		if samples == 1:
			byte_list[0] = 0x061 + (0b000 << 1)
		elif samples == 4:
			byte_list[0] = 0x061 + (0b001 << 1)
		elif samples == 16:
			byte_list[0] = 0x061 + (0b010 << 1)
		elif samples == 64:
			byte_list[0] = 0x061 + (0b011 << 1)
		elif samples == 128:
			byte_list[0] = 0x061 + (0b100 << 1)
		elif samples == 256:
			byte_list[0] = 0x061 + (0b101 << 1)
		elif samples == 512:
			byte_list[0] = 0x061 + (0b110 << 1)
		elif samples == 1024:
			byte_list[0] = 0x061 + (0b111 << 1)
		else:
			byte_list[0] = 0x061
		self.i2c.write_i2c_block_data(self.dev_address, self._INA260_CONFIG_ADDR, byte_list)
		