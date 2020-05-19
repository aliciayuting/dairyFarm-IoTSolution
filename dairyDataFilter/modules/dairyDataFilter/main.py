# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubModuleClient
import json

RECEIVED_MESSAGES = 0
THREASHOLD = {"Activity(steps/hr)": 300, "ActivityDeviation(%)": 100,
              "Fat(%)": 6, "Yield(gr)": 60000, "Protein(%)": 6, "ProductionRate(gr/hr)": 3000}
AVG = {"Activity(steps/hr)": 168, "ActivityDeviation(%)": 15.3, "Yield(gr)": 31644, "YieldDeviation(%)": 0, "Fat(%)": 0.14, "FatDeviation(%)": 10, "Protein(%)": 0.15, "ProteinDeviation(%)": 0,
       "Lactose(%)": 0.03, "LactoseDeviation(%)": 0, "Conductivity": 8, "ConductivityDeviation(%)": 0, "SCC (*1000/ml)": 43323005, "Blood(%)": 3.7, "ProductionRate(gr/hr)": 1307}


async def main():
    try:
        count = 0
        if not sys.version >= "3.5.3":
            raise Exception(
                "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version)
        print("IoT Hub Client for Python")

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()

        # define behavior for receiving an input message on input1
        # def input1_listener(module_client):
        print("******-------   Start data Filtering  ------****** ")
        while True:
            if count % 100 == 0:
                print("******-------   data continue Filtering  ------****** ")
            count += 1
            input_message = await module_client.receive_message_on_input("input1")
            # print("the data in the message received on input1 was ")
            # print(input_message.data)
            sample = input_message.data
            decoded_sample = sample.decode('utf-8')
            decoded_dict = json.loads(decoded_sample)
            data = decoded_dict['data'][0]
            result = {}
            result['ALERT'] = []
            for var in data:
                if var in THREASHOLD:
                    if var != None and data[var] != None and data[var] != "" and float(data[var]) > THREASHOLD[var]:
                        print("!! **  abnormal record - (" +
                              var+","+str(data[var])+")")
                        result['ALERT'].append(
                            [data["Date"], data["AnimalId"], var, data[var]])
                if data[var] == "":
                    data[var] = AVG[var]
            result['data'] = [data]
            j_data = json.dumps(result)
            output = bytes(j_data, encoding='utf8')
            # print(output)
            # print("forwarding mesage to output1")
            await module_client.send_message_to_output(output, "output1")

        # define behavior for halting the application
        # def stdin_listener():
        #     while True:
        #         try:
        #             selection = input("Press Q to quit\n")
        #             if selection == "Q" or selection == "q":
        #                 print("Quitting...")
        #                 break
        #         except:
        #             time.sleep(10)

        # # Schedule task for C2D Listener
        # listeners = asyncio.gather(input1_listener(module_client))

        # print("The sample is now waiting for messages. ")

        # # Run the stdin listener in the event loop
        # loop = asyncio.get_event_loop()
        # user_finished = loop.run_in_executor(
        #     None, input1_listener(module_client))

        # # Wait for user to indicate they are done listening for messages
        # await user_finished

        # # Cancel listening
        # listeners.cancel()

        # Finally, disconnect
        await module_client.disconnect()

    except Exception as e:
        print("Unexpected error %s " % e)
        raise

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    # asyncio.run(main())
