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
		self.rtype	= rtype
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
	def __init__(self, name: str = '@', ttl: str = 3600, data: str = '0.0.0.0'):
		if isinstance(ipaddress.ip_address(data), ipaddress.IPv4Address):
			self.data = data
		else:
			raise InvaliadDataException(message=f'{data} is not a valiad IPv4 Address.')

		self.rtype	= 'A'
		self.name	= name
		self.ttl	= ttl

@dataclass
class AAAA(Record):
	def __init__(self, name: str = '@', ttl: str = 3600, data: str = '0.0.0.0'):
		if isinstance(ipaddress.ip_address(data), ipaddress.IPv4Address):
			self.data = data
		else:
			raise InvaliadDataException(message=f'{data} is not a valiad IPv6 Address.')

		self.rtype	= 'AAAA'
		self.name	= name
		self.ttl	= ttl

@dataclass
class CNAME(Record):
	def __init__(self, name: str = '@', ttl: str = 3600, data: str = '0.0.0.0'):
		self.rtype	= 'CNAME'
		self.name	= name
		self.ttl	= ttl

		if(fqdn.FQDN(data).is_valid):
			self.data = data


@dataclass
class SOA(Record):
	def __init__(self, mname: str = 'ns1.example.com', rname: str = 'admin.example.com', serial: int = int(time.time()), refresh: int = 86400, retry: int = 7200, expire: int = 15552000, ttl: int = 21700):
		self.mname		= mname
		self.rname		= rname
		self.serial		= serial
		self.refresh	= refresh
		self.retry		= retry
		self.expire		= expire
		self.ttl		= ttl

	def __str__(self):
		return str(Record(self.name, self.ttl, f'{self.mname} {self.rname} {self.serial} {self.refresh} {self.retry} {self.expire} {self.ttl}'))

	mname: str		= 'ns1.example.com'
	rname: str		= 'admin.example.com'
	serial: int		= int(time.time())
	refresh: int	= 86400
	retry: int		= 7200
	expire: int		= 15552000
	ttl: int		= 21700

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

