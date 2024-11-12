import main

zone	= main.Zone(origin='example.com')
#soa		= main.SOA()
record	= main.Record(data='192.168.5.254', name='localhost.example.com')
#zone.add(soa)
zone.new_soa(mname='ns1.')
zone.add(record)
zone.add(main.A(name='example', data='fe80::727f:3322:18b1:23e7'))
zone.save_file('/tmp/zone.txt')