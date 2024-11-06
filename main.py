from enum import Enum
from dataclasses import dataclass, field
import time

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

	def new_soa(self, mname: str = 'ns1.example.com', rname: str = 'admin.example.com', serial: int = int(time.time()), refresh: int = 86400, retry: int = 7200, expire: int = 15552000, ttl: int = 21700):
		if mname[-1] != '.':
			mname = mname + '.' + self.origin
		self.add(SOA(mname=mname, rname=rname, serial=serial, refresh=refresh, retry=retry, expire=expire, ttl=ttl))

	def new_record(self, name: str = '@', ttl: str = 3600, rtype: str = 'A', data: str = '0.0.0.0'):
		if name[-1] != '.':
			name = name + '.' + self.origin
		self.add(name=name, ttl=ttl, rtype=rtype, data=data)

	def add(self, record: Record):
		self.records.append(record)

	def save_file(self, filepath: str):
		with open(filepath, 'w') as file:
			for record in self.records:
				file.write(str(record) + '\n')
				print(str(record))
		file.close()

