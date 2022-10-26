import requests
import json

'''
Use this for communicating with the isolated voltage source webserver
using python. Sending requests to the server this way, as opposed to 
communicating with the source directly via UDP, ensures that the
state of the source is remembered and accurately displayed in real time 
on any GUIs in the lab.

Andrew Mueller July 2022
'''


class IsolatedVSource:
    def __init__(self, serverIP, serverPort):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.post_url = f"http://{self.serverIP}:{self.serverPort}/submit"
        self.get_url = f"http://{self.serverIP}:{self.serverPort}/read"

    def set_voltage(self, channel, voltage, state = 'on'):
        packet = {
            "channel": str(int(channel)),
            "voltage": voltage,
            "state": state
        }
        ret = requests.post(url = self.post_url, data = json.dumps(packet))
        print(ret)
        # print(ret.text)

    def get_voltage(self, channel):
        packet = {
            "channel": int(channel),
        }
        ret = requests.get(url = self.get_url, params=packet)
        # print(ret.url)
        # print(ret)
        obj = json.loads(ret.text)
        print(obj)
        return obj

if __name__ == "__main__":
    source = IsolatedVSource('10.7.0.137', 8000)
    source.set_voltage(1,0.555, state = 'on')
    # source.get_voltage(1)
