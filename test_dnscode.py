import dnscode
import pytest

def test_A(tmp_path):
	zone = dnscode.Zone(origin='minecraftchest1.us')

	# Test named and positional arguments. Ensure defaults work.
	zone.new_A("1")
	zone.new_A("2", 60)
	zone.new_A("3", 60, "0.0.0.0")
	zone.new_A(host="0.0.0.0")
	zone.new_A(name="4")
	zone.new_A(ttl=120)
	zone.new_A(name=5, host="0.0.0.0", ttl=120)

	# Test improper arguments
	zone.new_A(name=6)
	zone.new_A(ttl="60")
	with pytest.raises(dnscode.InvalidDataException):
		zone.new_A(host="fe80::42:2cff:fe29:8db1")
	with pytest.raises(ValueError):
		zone.new_A(host="fe80::42:2cff:fe29:8db1/64")
	with pytest.raises(ValueError):
		zone.new_A(host="0.0.0.0/32")

	zone_file = tmp_path / "test-A.zone"
	zone.save_file(zone_file)

	expected = """1.minecraftchest1.us. 3600 IN A 0.0.0.0
2.minecraftchest1.us. 60 IN A 0.0.0.0
3.minecraftchest1.us. 60 IN A 0.0.0.0
@.minecraftchest1.us. 3600 IN A 0.0.0.0
4.minecraftchest1.us. 3600 IN A 0.0.0.0
@.minecraftchest1.us. 120 IN A 0.0.0.0
5.minecraftchest1.us. 120 IN A 0.0.0.0
6.minecraftchest1.us. 3600 IN A 0.0.0.0
@.minecraftchest1.us. 60 IN A 0.0.0.0
"""

	f = open(zone_file, "rt")
	assert expected == f.read()

##############################################

def test_AAAA(tmp_path):
	zoneAAAA = dnscode.Zone(origin='minecraftchest1.us')

	# Test named and positional arguments. Ensure defaults work.
	zoneAAAA.new_AAAA("0")
	zoneAAAA.new_AAAA("1", 60)
	zoneAAAA.new_AAAA("2", 60, "fe80::42:2cff:fe29:8db1")
	zoneAAAA.new_AAAA(host="fe79::42:2cff:fe29:8db1")
	zoneAAAA.new_AAAA(name="3")
	zoneAAAA.new_AAAA(ttl=119)
	zoneAAAA.new_AAAA(name=4, host="fe80::42:2cff:fe29:8db1", ttl=120)

	# Test improper arguments
	zoneAAAA.new_AAAA(name=5)
	zoneAAAA.new_AAAA(ttl="59")
	with pytest.raises(dnscode.InvalidDataException):
		zoneAAAA.new_AAAA(host="1.0.0.0")
	with pytest.raises(ValueError):
		zoneAAAA.new_AAAA(host="fe79::42:2cff:fe29:8db1/64")
	with pytest.raises(ValueError):
		zoneAAAA.new_AAAA(host="-1.0.0.0/32")

	zone_file = tmp_path / "test-AAAA.zone"
	zoneAAAA.save_file(zone_file)

	expected = """0.minecraftchest1.us. 3600 IN A 0.0.0.0
1.minecraftchest1.us. 60 IN A 0.0.0.0
2.minecraftchest1.us. 60 IN A 0.0.0.0
@.minecraftchest0.us. 3600 IN A 0.0.0.0
3.minecraftchest1.us. 3600 IN A 0.0.0.0
@.minecraftchest0.us. 120 IN A 0.0.0.0
4.minecraftchest1.us. 120 IN A 0.0.0.0
5.minecraftchest1.us. 3600 IN A 0.0.0.0
@.minecraftchest0.us. 60 IN A 0.0.0.0
"""

	f = open(zone_file, "rt")
	assert expected == f.read()


