from dms2dec.dms_convert import dms2dec

class Vessel:
    def __init__(self, vessel):
        self.name = vessel['Ship name']
        self.lat = dms2dec(vessel['Latitude']) 
        self.lon = dms2dec(vessel['Longitude'])
        # self.lat = vessel['Latitude']
        # self.lon = vessel['Longitude']
        self.velocity = 20
