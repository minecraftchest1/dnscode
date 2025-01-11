from enum import Enum
from dataclasses import dataclass, field
import time
import ipaddress
import dns
import fqdn

class InvaliadDataException(Exception):
	"""Exception raied when invaliad data is passed to a record"""

	def __init__(self, message):
		self.message	= message
		super().__init__(self, message)

@dataclass
class Record:
	def __int__(self, name: str = '@', ttl: str = 3600, rtype: str = 'A', data: str = '0.0.0.0'):
		self.rtype: str	= rtype
		self.name	= name
		self.data	= data
		self.ttl	= ttl

	def __str__(self):
		return f"{self.name} {self.ttl} {self.rclass} {self.rtype} {self.data}"

	rclass: str = 'IN'
	rtype: str	= 'A'
	name: str	= '@'
	data: str	= '0.0.0.0'
	ttl: int	= 6400

@dataclass
class A(Record):
	def __init__(self, name: str = '@', ttl: str = 3600, target: str = '0.0.0.0'):
		if isinstance(ipaddress.ip_address(data), ipaddress.IPv4Address):
			self.data = data
		else:
			raise InvaliadDataException(message=f'{data} is not a valid IPv4 Address.')

		self.rtype	= 'A'
		self.name	= name
		self.ttl	= ttl

@dataclass
class AAAA(Record):
	def __init__(self, name: str = '@', ttl: str = 3600, target: str = '0.0.0.0'):
		if isinstance(ipaddress.ip_address(data), ipaddress.IPv4Address):
			self.data = data
		else:
			raise InvaliadDataException(message=f'{data} is not a valiad IPv6 Address.')

		self.rtype	= 'AAAA'
		self.name	= name
		self.ttl	= ttl

@dataclass
class CNAME(Record):
	def __init__(self, name: str = '@', ttl: str = 3600, target: str = '0.0.0.0'):
		self.rtype	= 'CNAME'
		self.name	= name
		self.ttl	= ttl

		if(fqdn.FQDN(target).is_valid):
			self.data = target
		else:
			raise InvaliadDataException

@dataclass
class MX(Record):
	def __init__(self, name: str = '@', ttl: str = 3600, priority: int = '10', host: str = 'example.com'):
		self.rtype	= 'MX'
		self.name	= name
		self.ttl	= ttl
		self.priority	= priority
		self.data	= "{ttl} {priority}"

		if(fqdn.FQDN(host).is_valid):
			self.host = host
		else:
			raise InvaliadDataException(message='{host} is not a valid FQDN')

@dataclass
class NS(Record):
	def __init__(self, name: str = '@', ttl: str = 3600, target: str = 'example.com'):
		self.rtype	= 'MX'
		self.name	= name
		self.ttl	= ttl

		if (fqdn.FQDN(host).is_valid):
			self.host = host
		else:
			raise InvaliadDataException(message='{target} is nod a valid FQDN')
		self.data	= target

@dataclass
class PTR(Record):
	def __init__(self, name: str = '@', ttl: str = 3600, host: str = '0.0.0.0'):
		self.rtype	= 'PTR'
		self.name	= name
		self.ttl	= ttl

		if(fqdn.FQDN(host).is_valid):
			self.data = host
		else:
			raise InvaliadDataException(message='{host} is not a valid FQDN')

# TODO: Cleanup. I have no idea why I have _str_() defined.
@dataclass
class SOA(Record):
	def __init__(self, name: str = '@', mname: str = 'ns1.example.com', rname: str = 'admin.example.com',
				serial: int = int(time.time()), refresh: int = 86400, retry: int = 7200,
				expire: int = 15552000, ttl: int = 21700
		):
		self.rtype		= "SOA"
		self.name		= name
		self.mname		= mname
		self.rname		= rname
		self.serial		= serial
		self.refresh	= refresh
		self.retry		= retry
		self.expire		= expire
		self.ttl		= ttl
		self.data		= "{name} {ttl} IN SOA {mname} {rname} {serial} {refresh} {retry} {expire} {ttl}"

@dataclass
class SRV(Record):
	def __int__(self, name: str = '@', ttl: str = 3600, service: str = "service", protocol: str = 'proto',
				priority: int = 10, weight: int = 10, port: int = 0, target: str = target
				):
		self.rtype	= 'PTR'
		self.name	= '_{service}._{protocol}.name'
		self.ttl 	= ttl
		self.service	= service
		self.protocol	= protocol
		self.priority	= priority
		self.weight		= weight
		self.port	= port
		if (fqdn.FQDN(host).is_valid):
			self.target	= target
		else:
			raise InvaliadDataException(message='{target} is not a valiad FQDN')
		self.data	= "{priority} {weight} {port} {target}"

@dataclass
class Zone:
	origin: str
	records: list = field(default_factory=list)

	def __str__(self):
		zone: str = ''

		for record in self.records:
			zone.join(record)

		return zone

	def __mkfqdn(self, name):
		if name[-1] != '.':
			return name + '.' + self.origin
		else:
			return name

	def new_A(self, name: str = '@', ttl: int = 3600, data: str = '0.0.0.0'):
		name = self.__mkfqdn(name)
		self.add(A(name=name, ttl=ttl, data=data))

	def new_AAAA(self, name: str = '@', ttl: int = 3600, data: str = '0.0.0.0'):
		name = self.__mkfqdn(name)
		self.add(AAAA(name=name, ttl=ttl, data=data))

	def new_CNAME(self, name: str = '@', ttl: int = 3600, data: str = '0.0.0.0'):
		name = self.__mkfqdn(name)
		self.add(CNAME(name=name, ttl=ttl, data=data))

	def new_MX(self, name: str = '@', ttl: int = 3600, priority: int = 10, host: str = 'example.com'):
		name = self.__mkfqdn(name)
		self.add(MX(name=name, ttl=ttl, priority=priority, host=host))

	def new_soa(self, mname: str = 'ns1.example.com', rname: str = 'admin.example.com', serial: int = int(time.time()), refresh: int = 86400, retry: int = 7200, expire: int = 15552000, ttl: int = 21700):
		mname = self.__mkfqdn(name)
		self.add(SOA(mname=mname, rname=rname, serial=serial, refresh=refresh, retry=retry, expire=expire, ttl=ttl))

	def new_record(self, name: str = '@', ttl: int = 3600, rtype: str = 'A', data: str = '0.0.0.0'):
		name = self.__mkfqdn(name)
		self.add(name=name, ttl=ttl, rtype=rtype, data=data)

	def add(self, record: Record):
		self.records.append(record)

	def save_file(self, filepath: str):
		with open(filepath, 'w') as file:
			for record in self.records:
				file.write(str(record) + '\n')
				print(str(record))
		file.close()

