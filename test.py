import main

zone	= main.Zone()
soa		= main.SOA()
record	= main.Record(data='192.168.5.254', name='localhost.example.com')
zone.add(soa)
zone.add(record)
zone.save_file('/tmp/zone.txt')