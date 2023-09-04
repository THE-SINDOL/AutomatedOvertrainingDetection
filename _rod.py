import gdown
import json
import linecache
import math
import os
import requests
import sys
import time

print("""
 ___          _ _   _             ___              _            _      _            ___      _          _   _          
| _ \___ __ _| | |_(_)_ __  ___  / _ \__ _____ _ _| |_ _ _ __ _(_)_ _ (_)_ _  __ _ |   \ ___| |_ ___ __| |_(_)___ _ _  
|   / -_) _` | |  _| | '  \/ -_)| (_) \ V / -_) '_|  _| '_/ _` | | ' \| | ' \/ _` || |) / -_)  _/ -_) _|  _| / _ \ ' \ 
|_|_\___\__,_|_|\__|_|_|_|_\___| \___/ \_/\___|_|  \__|_| \__,_|_|_||_|_|_||_\__, ||___/\___|\__\___\__|\__|_\___/_||_|
                                                                              |___/                                    
Author: grvyscale
 """)  # PRINT LOGO

# CONFIG
with open('config.json', 'r') as configfile:
    try:
        config = json.load(configfile)
    except json.JSONDecodeError as JSONDecodeError:
        print(f"\033[31mConfig Invalid Syntax: ")
        input(f"{JSONDecodeError}")
        sys.exit()
    modelname, iterations, refreshrate, environment, download = config.values()

    def verifyConfig(VCvalue, VCcondition):
        if not VCcondition(VCvalue):
            input("\033[31mInvalid Config, press ENTER to exit.")
            sys.exit()
    # region    VERIFICATION CONDITIONS
    verifyConfig((modelname), lambda x: isinstance(x, str) and x != "")
    verifyConfig((iterations), lambda x: isinstance(x, int) and 1 <= x <= 1000)
    verifyConfig((refreshrate), lambda x: isinstance(x, int) and 1 <= x)
    verifyConfig((environment), lambda x: isinstance(x, str) and x == "local" or x == "colab")
    # endregion

# PRE-DEFINED VARIABLES
temp = os.path.join((os.getcwd()), "temp", f"{environment}", f"{modelname}")
logs = os.path.join((os.getcwd()), "logs", "[ROD]", f"{modelname}")



def main():
    # RESET VARIABLE
    epochs = []
    weights = []
    averageWeight = 0
    averageEpoch = 0
    average = 0

    # UPDATE TEMP DIRECTORY
    if not os.path.exists(temp):
        os.makedirs(temp)
    else:
        for tempFiles in os.listdir(temp):
            tempFilesPath = os.path.join(temp, tempFiles)
            os.remove(tempFilesPath)
    # UPDATE LOGS DIRECTORY
    if not os.path.exists(logs):
        os.makedirs(logs)
    else:
        for logsFiles in os.listdir(logs):
            logsFilesPath = os.path.join(logs, logsFiles)
            os.remove(logsFilesPath)

    # IMPORT DATA
    if environment == "local":
        # download scalar
        try:
            url = f"http://localhost:6006/data/plugin/scalars/scalars?tag=loss%2Fg%2Ftotal&run={modelname}&format=csv"
            response = requests.get(url)
            lines = response.text.strip().split('\n')
            for line in lines[1:]:
                delims = line.split(',')
                if len(delims) >= 3:
                    step = delims[1].strip()
                    raw = delims[2].strip()
                    with open(f"{temp}\\step.txt", "a") as stepFile:
                        stepFile.write(step + '\n')
                    with open(f"{temp}\\raw.txt", "a") as rawFile:
                        rawFile.write(raw + '\n')
        except requests.RequestException as RequestsException:
            input("\033[31mTensorBoard: failed to download")

    if environment == "colab":
        # import events files
        gdNameIndex = 0
        for gdLink in download:
            gdNameIndex += 1
            gdName = f"events.out.tfevents.{gdNameIndex}.0"
            gdId = gdLink.split('/')[-2]
            gdown.download(f"https://drive.google.com/uc?/export=download&id={gdId}", f"{logs}\\{gdName}", quiet=False)

        # wait until events are imported
        while True:
            time.sleep(0.5)
            if os.path.exists(f"{logs}\\{gdName}"):
                break

        # download scalar
        try:
            url = f"http://localhost:6006/data/plugin/scalars/scalars?tag=loss%2Fg%2Ftotal&run=[ROD]\\{modelname}&format=csv"
            response = requests.get(url)
            lines = response.text.strip().split('\n')
            for line in lines[1:]:
                delims = line.split(',')
                if len(delims) >= 3:
                    step = delims[1].strip()
                    raw = delims[2].strip()
                    with open(f"{temp}\\step.txt", "a") as stepFile:
                        stepFile.write(step + '\n')
                    with open(f"{temp}\\raw.txt", "a") as rawFile:
                        rawFile.write(raw + '\n')
        except requests.RequestException as RequestsException:
            input("\033[31mTensorBoard: failed to download")

    # WAIT UNITL (RAW, STEP) EXIST
    while True:
        time.sleep(0.5)
        if os.path.exists(f"{temp}\\raw.txt") and os.path.exists(f"{temp}\\step.txt"):
            break

    # SMOOTH VALUES
    for smoothing in range(1000):
        smoothing /= 1000

        def smooth(smoothing):
            # import data
            dataset = {'data': []}
            with open(f"{temp}\\raw.txt", 'r') as file:
                dataset['data'] = [{'y': float(line.strip())} for line in file]

            # smooth dataset
            data = dataset['data']
            last = 0 if len(data) > 0 else float('nan')
            num_accum = 0
            y_values = [d['y'] for d in data]
            is_constant = all(v == y_values[0] for v in y_values)
            for i, d in enumerate(data):
                next_val = y_values[i]
                if is_constant or not (isinstance(next_val, (int, float)) and not math.isnan(next_val)):
                    d['smoothed'] = next_val
                else:
                    last = last * smoothing + (1 - smoothing) * next_val
                    num_accum += 1
                    debias_weight = 1
                    if smoothing != 1:
                        debias_weight = 1 - math.pow(smoothing, num_accum)
                    d['smoothed'] = last / debias_weight

            # export dataset
            with open(f"{temp}\\smoothed{smoothing}.txt", 'w') as file:
                file.write('\n'.join(map(str, [d['smoothed'] for d in dataset['data']])))

        smooth(smoothing)

    # CHECK IF THERE ARE ENOUGH VALUES AFTER LOWEST POINT (REALTIME)
    rawMin = float('inf')
    with open(f"{temp}\\raw.txt", 'r') as rawFile:
        for rawIndex, rawLine in enumerate(rawFile, start=1):
            rawRead = float(rawLine.strip())
            if rawRead < rawMin:
                rawMin = rawRead
                rawLowPoint = rawIndex
    for loop in range(0, iterations):
        rawLowPoint += 1
        next_line = linecache.getline(f"{temp}\\raw.txt", rawLowPoint)

        if next_line == "":
            print(
                f"\033[31mNo Value Provided, Refreshing in {refreshrate}")
            time.sleep(refreshrate)
            main()

    # GET LOWEST POINTS
    lastIndex = -1
    for smoothing in range(1000):
        smoothedMin = float('inf')
        currentIndex = -1
        smoothing /= 1000
        with open(f"{temp}\\smoothed{smoothing}.txt", 'r') as smoothedFile:
            for smoothedIndex, smothedLine in enumerate(smoothedFile, start=1):
                smoothedRead = float(smothedLine.strip())
                if smoothedRead < smoothedMin:
                    smoothedMin = smoothedRead
                    currentIndex = smoothedIndex
                    currentIndex -= 1
        if lastIndex != -1:
            if currentIndex != lastIndex:
                epochs.append(currentIndex)
                weights.append(smoothing)
        lastIndex = currentIndex

    # CALCULATE WEIGHTED AVERAGE
    dictionary = zip(epochs, weights)
    for epoch, weight in dictionary:
        averageEpoch += epoch * weight
        averageWeight += weight
    average = averageEpoch / averageWeight
    return average

print(f"\033[92mEPOCH: {int(main())}\033[0m")
input("\033[90mFinished! Press ENTER to exit.\033[0m")
