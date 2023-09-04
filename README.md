# Realtime Overtraining Detection (ROD) GUIDE

Simple program that will automate searching the most optimal
epoch for your RVC model


## Download Rod
1. Ensure you have [**Python**](https://www.python.org/downloads/) installed. 
2. Go to the [Releases](https://github.com/grvyscale/RealtimeOvertrainingDetection/releases) tab.
3. Download the latest version of ROD (rod.zip).


## Unpack the Files
Unzip the downloaded rod.zip file to a location of your choice.


### Local Training:
- If you plan to train locally, create a directory in your "Mangio-RVC".
- Drop the unpacked ROD files inside the created directory.


### Colab Training:
- If you're using Google Colab, simply unzip the files and keep them in the same directory.


## Install Requirements
Run the `install-requirements.bat` script to install the necessary dependencies.


## Creating Configuration File
Use the `modify-config.bat` script to create and edit a configuration file according to your needs.


### Personalizing Your Config
**Model Name** serves as the identifier for monitoring on the specified model.


**Iterations** Iterations determine the number of epochs that should be after reaching lowest point on the graph. 
For instance, if you select 100 iterations and there are only 20 epochs after lowest point, 
it will refresh after specified number of seconds.

IF YOU ALREADY HAVE TRAINED MODEL SET ITERATIONS TO 1


**Refresh Rate** The refresh rate indicates how frequently the program will update itself in seconds,
if there is no value provided.

**Environment**  Specifies your current workspace, 
offering two options: 'local' or 'colab.' 
When utilizing 'colab,' you will need to input specific links to the 'events.out.tfevents.0' files stored in your Google Drive.
Which can be found by going to these directories:
- RVC_Backup
- YOUR MODEL NAME

Additionally, ensure that permissions are configured to allow anyone with the link to download these files.


## Launch Tensorboard
Start Tensorboard by running the `launch-tensorboard.bat` script.


## Run rod.bat
execute the `rod.bat` script, and get the outcome of sufficient epochs number.
