import dbus, time
 
service_record = """
<?xml version="1.0" encoding="UTF-8" ?>
<record>
  <attribute id="0x0001">
    <sequence>
      <uuid value="0x1101"/>
    </sequence>
  </attribute>
  <attribute id="0x0004">
    <sequence>
      <sequence>
        <uuid value="0x0100"/>
      </sequence>
      <sequence>
        <uuid value="0x0003"/>
        <uint8 value="1" name="channel"/>
      </sequence>
    </sequence>
  </attribute>
  <attribute id="0x0100">
    <text value="Serial Port" name="name"/>
  </attribute>
</record>
"""
 
bus = dbus.SystemBus()
manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"),
                        "org.bluez.ProfileManager1")
manager.RegisterProfile("/bluez",
                        "00001101-0000-1000-8000-00805f9b34fb",
                        {"AutoConnect":True, "ServiceRecord":service_record})
while True:
    time.sleep(1)
