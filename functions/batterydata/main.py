import json
import logging
import sys

def convertbatterydata(payload):
    state_map = {
        0: "power off",
        1: "power on",
        2: "discharge",
        3: "charge",
        4: "charge complete",
        5: "host mode",
        6: "shutdown",
        7: "error",
        8: "undefined"
    }
    #since the encoding is in little endian the values are stored in opposite order of the memory address
    #so making it in big indian for sake of simplicity
    #in this function byte order is reversed
    def convert_little_endian_to_big_indian_encoding(hex):
        #using bit operations to modify encoding
        ba = bytearray.fromhex(hex)
        ba.reverse()
        return str(ba.hex())
    
    #making the payload to big endian encoding
    payload = convert_little_endian_to_big_indian_encoding(payload)

    # since using bit conversion to int for the values
    # data will be of format 00BBCCSTTTTTTTTX
    #                        0123456789ABCDEF 
    #so we are getting the payload and dividing it into required pieces 
    type = int( payload[15] ,16)
    time= int(payload[7:15] ,16)
    state = state_map[int(payload[6] ,16)] 
    state_of_charge = int( payload[4:6], 16)
    battery_temprature = int(payload[2:4],16)
    
    #encapsulating the values in dict to return 
    return {   
        "time" : time,
        "state" : state,
        "state_of_charge" : state_of_charge/2,
        "temperature": battery_temprature/2 - 20
    }


def battery_device_wrapper(device, payload):
    processed_data = convertbatterydata(payload)
    processed_data["device"] = device 
    return processed_data


def handler(event, context):
    processed_data =  battery_device_wrapper(event["device"],event["payload"])
    
    #logging data to the system 
    sys.stdout.write(json.dumps(processed_data))

    # returning the data
    return processed_data



if __name__ == "__main__":
    pass