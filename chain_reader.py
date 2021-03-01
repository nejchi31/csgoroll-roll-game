import matplotlib.pyplot as plt
import numpy as np
import hashlib
import random
import string
import hmac
import csv

#clientSeed = '1b2335a656a2d9f43295582daec6d19e3ea4a957e615b56da386e30f78324eba'
#serverSeed = '97a9fad9f527d28105c0c2adc3c44935790b0b5b7d0e2eafa12ccad15dab2349'
#start_nonce = 1353737
#end_nonce = 1357379

def get_result(game_hash):
    subHash = game_hash[0:8]
    spinNumber  = int(subHash, 16)
    return abs(spinNumber) % 15

def getRollSpin(serverSeed, clientSeed, nonce):
    seed = getCombinedSeed(serverSeed, clientSeed, nonce)
    hm = hmac.new(seed.encode(), b'', hashlib.sha256)
    return hm.hexdigest()

def getCombinedSeed(serverSeed, clientSeed, nonce):
    return serverSeed + '-' + clientSeed + '-' + str(nonce)


def getRollColour(roll):
    if(roll == 0):
        return 'Green'
    if(roll <= 7 and roll >= 1):
        return 'Red'
    else:
        return 'Black'


def export_data_to_file(serverSeed, clientSeed, nonce, end_nonce):
    results = []
    count = 0
    with open('DATASET_14-2_1-3-color.csv', 'a', newline='') as fd:
        nonce = nonce
        end_nonce = end_nonce
        while nonce <= end_nonce:
            temp = getRollSpin(serverSeed,clientSeed, nonce)
            roll_result = getRollColour(get_result(temp)) #get_result(temp) #
            results.append(roll_result)
            writerdata = csv.writer(fd)
            writerdata.writerow([roll_result])
            nonce += 1
    fd.close()
    return np.array(results)

def import_inputs_to_workspace():
    inputs = []
    with open('roll-inputs.csv', 'r', newline='') as fd:
        reader = csv.reader(fd, delimiter = ',')
        for row in reader:
            inputs.append(row)
        fd.close()
    return inputs


for data in import_inputs_to_workspace():
    export_data_to_file(data[0], data[1], int(data[2]), int(data[3]))

