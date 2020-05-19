# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
import time
import os
import sys
import asyncio
# from six.moves import input
import threading
from azure.iot.device.aio import IoTHubModuleClient
import csv
import json

filepath = './test_dairy_data.csv'
# cow_cols = ["datesql",  "Animal_ID"]
# # note the last few cols are one-hot encoding of "Gynecology_Status" : ['Abortion', 'Fresh (Calving)', 'Heat', 'Insemination', 'Not for Insemination','Pregnant']
# health_cols = ['Blood(%)', 'Avg_Milking_Time(seconds)', 'RestBout(#)', 'RestRatio(%)', 'RestTime(min)', 'Weight(gr)',
#                "AnimalStatus", 'Abortion', 'Fresh (Calving)', 'Heat', 'Insemination', 'Not for Insemination', 'Pregnant']
# activity_cols = ['DIM', 'Activity(steps/hr)', 'ActivityDeviation(%)',
#                  'Yield(gr)', 'ProdRate(gr/hr)', 'Activity(steps/hr)', 'ActivityDeviation(%)']
# milk_cols = ['Protein(%)', "Fat(%)", 'Lactose', 'Conductivity']

# filtered_columns = cow_cols+health_cols+activity_cols+milk_cols+["IsEstrus"]
filtered_columns = []


async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception(
                "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version)
        print("IoT Hub Client for Python")

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()
        print("IoT Hub module client initialized.")
        with open(filepath, mode='r') as dairy_file:
            while True:
                start = 0
                dairy_reader = csv.reader(dairy_file, delimiter=',')
                filter = []
                f_cols = []
                for row in dairy_reader:
                    time.sleep(10)
                    if start == 0:
                        print(start)
                        filter = [i for i in range(len(row))]
                        f_cols = [col for col in row]
                        # filter = [i for i in range(
                        #     len(row)) if row[i] in filtered_columns]
                        # f_cols = [filtered_columns.index(col) for col in row]
                        print(filter)
                    else:
                        print(
                            "  **************  -----   new farm record  -----   **************")
                        msg = [row[index] for index in filter]
                        print(filter)
                        # print(msg)
                        data = {}
                        for i in range(len(filter)):
                            print(f_cols[i])
                            data[f_cols[i]] = msg[i]
                        print(f_cols)
                        j_data = json.dumps({'data': [data]})
                        output = bytes(j_data, encoding='utf8')

                        # send to next client
                        await module_client.send_message_to_output(output, "outputs")
                    start += 1

        # def stdin_listener():
        #     while True:
        #         try:
        #             selection = input("Press Q to quit\n")
        #             if selection == "Q" or selection == "q":
        #                 print("Quitting...")
        #                 break
        #         except:
        #             time.sleep(10)

        # Schedule task for C2D Listener
        # listeners = asyncio.gather(input1_listener(module_client))

        # print("The sample is now waiting for messages. ")

        # Run the stdin listener in the event loop
        # loop = asyncio.get_event_loop()
        # user_finished = loop.run_in_executor(None, stdin_listener)

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
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    asyncio.run(main())
