# CyPsa
CyPsa Tool

## Prerequisites
* [Apache Ant](http://ant.apache.org/manual/install.html)

## Getting Started
If you want to use CYPSA for a utility dataset, here is what you do.  
* `ant new -Dutility=utility name`.  Create a directory structure for the utility dataset in the build directory.  This syntax is clunky.
* Manually populate the dataset using the directories provided.
* `ant run-cypsa`.  Run all CYPSA services using the utility data.

### Manually Populating Data ###
In this working tutorial, we now talk about each of the folders and their purposes.
The root directory for this conversation will be found in `build/UTILITY_NAME`.

As a working example, we will use the 8-substation model.

#### Firewall ####
Contains all firewall rulesets.

#### NMap ####
Contains all nmap scans.  For the control center or substation?

#### PowerWorld ####
Contains case.pwb for that utility.

#### Cyber Physical Interconnect ####
Contains a CSV file of the interconnect file.  Consists of RelayID, RelayIP, and BreakerIDs

#### State ####
Contains the state of the relays (e.g. badger is one example)

#### Physical ####
Contains images, GPS, etc.

Notes: 
Copied folder 8bus-August2015 and renamed it to 8bus. 
Copied file critical-assets and renamed it to critical_assets.txt.
These are hard coded into the current version of the SOCCA engine (CPPW). 
After making these changes, the script runs sucessfully
	runCyPSA.bat 8bus 

I've started modifiying the SOCCA engine code so that these files can be specified in a configuration
file.

### Prerequisites
1. Check the configuration file: C:\CyPsaProduction\bin\CyPsaEngine\config.dat
2. Launch web ui by running php webserver and going to http://localhost/test4.php

### 8bus analysis
3. From the command line, in C:\CyPsaProduction\bin, type runCyPSA 8bus

### Results and Patching
4. Attack graph gets updated here: C:\CyPsaProduction\projects\8bus\attack_graph

Notes to run 8-bus analysis:

Notes to patch compromise:
