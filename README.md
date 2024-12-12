
# `Inertial Data Synthesis of Drivers with Mutiple Behavioral Patterns`

This project was developed as part of the Cognitive Architectures research line from 
the Hub for Artificial Intelligence and Cognitive Architectures (H.IAAC) of the State University of Campinas (UNICAMP).
See more projects from the group [here](https://github.com/brgsil/RepoOrganizer).

[![](https://img.shields.io/badge/-H.IAAC-eb901a?style=for-the-badge&labelColor=black)](https://hiaac.unicamp.br/)
[![](https://img.shields.io/badge/-Arq.Cog-black?style=for-the-badge&labelColor=white&logo=data:image/svg%2bxml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4gPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1Ni4wMDQiIGhlaWdodD0iNTYiIHZpZXdCb3g9IjAgMCA1Ni4wMDQgNTYiPjxwYXRoIGlkPSJhcnFjb2ctMiIgZD0iTTk1NS43NzQsMjc0LjJhNi41Nyw2LjU3LDAsMCwxLTYuNTItNmwtLjA5MS0xLjE0NS04LjEtMi41LS42ODksMS4xMjNhNi41NCw2LjU0LDAsMCwxLTExLjEzNi4wMjEsNi41Niw2LjU2LDAsMCwxLDEuMzY4LTguNDQxbC44LS42NjUtMi4xNS05LjQ5MS0xLjIxNy0uMTJhNi42NTUsNi42NTUsMCwwLDEtMi41OS0uODIyLDYuNTI4LDYuNTI4LDAsMCwxLTIuNDQzLTguOSw2LjU1Niw2LjU1NiwwLDAsMSw1LjctMy4zLDYuNDU2LDYuNDU2LDAsMCwxLDIuNDU4LjQ4M2wxLC40MSw2Ljg2Ny02LjM2Ni0uNDg4LTEuMTA3YTYuNTMsNi41MywwLDAsMSw1Ljk3OC05LjE3Niw2LjU3NSw2LjU3NSwwLDAsMSw2LjUxOCw2LjAxNmwuMDkyLDEuMTQ1LDguMDg3LDIuNS42ODktMS4xMjJhNi41MzUsNi41MzUsMCwxLDEsOS4yODksOC43ODZsLS45NDcuNjUyLDIuMDk1LDkuMjE4LDEuMzQzLjAxM2E2LjUwNyw2LjUwNywwLDAsMSw1LjYwOSw5LjcyMSw2LjU2MSw2LjU2MSwwLDAsMS01LjcsMy4zMWgwYTYuNCw2LjQsMCwwLDEtMi45ODctLjczMmwtMS4wNjEtLjU1LTYuNjgsNi4xOTIuNjM0LDEuMTU5YTYuNTM1LDYuNTM1LDAsMCwxLTUuNzI1LDkuNjkxWm0wLTExLjQ2MWE0Ljk1LDQuOTUsMCwxLDAsNC45NTIsNC45NUE0Ljk1Nyw0Ljk1NywwLDAsMCw5NTUuNzc0LDI2Mi43MzlaTTkzNC44LDI1Ny4zMjVhNC45NTIsNC45NTIsMCwxLDAsNC4yMjEsMi4zNDVBNC45Myw0LjkzLDAsMCwwLDkzNC44LDI1Ny4zMjVabS0uMDIyLTEuNThhNi41MTQsNi41MTQsMCwwLDEsNi41NDksNi4xTDk0MS40LDI2M2w4LjA2MSwyLjUuNjg0LTEuMTQ1YTYuNTkxLDYuNTkxLDAsMCwxLDUuNjI0LTMuMjA2LDYuNDQ4LDYuNDQ4LDAsMCwxLDIuODQ0LjY1bDEuMDQ5LjUxOSw2LjczNC02LjI1MS0uNTkzLTEuMTQ1YTYuNTI1LDYuNTI1LDAsMCwxLC4xMTUtNi4yMjksNi42MTgsNi42MTgsMCwwLDEsMS45NjYtMi4xMzRsLjk0NC0uNjUyLTIuMDkzLTkuMjIyLTEuMzM2LS4wMThhNi41MjEsNi41MjEsMCwwLDEtNi40MjktNi4xbC0uMDc3LTEuMTY1LTguMDc0LTIuNS0uNjg0LDEuMTQ4YTYuNTM0LDYuNTM0LDAsMCwxLTguOTY2LDIuMjY0bC0xLjA5MS0uNjUyLTYuNjE3LDYuMTMxLjc1MSwxLjE5MmE2LjUxOCw2LjUxOCwwLDAsMS0yLjMsOS4xNjRsLTEuMS42MTksMi4wNiw5LjA4NywxLjQ1MS0uMUM5MzQuNDc1LDI1NS43NSw5MzQuNjI2LDI1NS43NDQsOTM0Ljc3OSwyNTUuNzQ0Wm0zNi44NDQtOC43NjJhNC45NzcsNC45NzcsMCwwLDAtNC4zMTYsMi41LDQuODg5LDQuODg5LDAsMCwwLS40NjQsMy43NjIsNC45NDgsNC45NDgsMCwxLDAsNC43NzktNi4yNjZaTTkyOC43LDIzNS41MzNhNC45NzksNC45NzksMCwwLDAtNC4zMTcsMi41LDQuOTQ4LDQuOTQ4LDAsMCwwLDQuMjkxLDcuMzkxLDQuOTc1LDQuOTc1LDAsMCwwLDQuMzE2LTIuNSw0Ljg4Miw0Ljg4MiwwLDAsMCwuNDY0LTMuNzYxLDQuOTQsNC45NCwwLDAsMC00Ljc1NC0zLjYzWm0zNi43NzYtMTAuMzQ2YTQuOTUsNC45NSwwLDEsMCw0LjIyMiwyLjM0NUE0LjkyMyw0LjkyMywwLDAsMCw5NjUuNDc5LDIyNS4xODdabS0yMC45NTItNS40MTVhNC45NTEsNC45NTEsMCwxLDAsNC45NTEsNC45NTFBNC45NTcsNC45NTcsMCwwLDAsOTQ0LjUyNywyMTkuNzcyWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTkyMi4xNDMgLTIxOC4yKSIgZmlsbD0iIzgzMDNmZiI+PC9wYXRoPjwvc3ZnPiA=)](https://github.com/brgsil/RepoOrganizer)

## Repository Structure

Each folder contains similar files, but with different maps for SUMO, except for the tests folder. The folders that are not listed below were used only for testing on different maps and might not be fully working.

Note that each folder is a project on its own and does not depend on any other folders.

Later versions of the repository will be better organized.

- scripts: folder containing scrips that are used for every map, such as calls to APIs.
- unicamp/unv: folder containing files related to the university maps.
- testes: folder containing experiments, currently running mermaid to check for variability in trip generation.

## Dependencies / Requirements

The only requirement to use this repository is having SUMO installed and an environment variable set for `GROQ_API_KEY` (create your key at https://console.groq.com). The documentation for the installation can be found at: https://sumo.dlr.de/docs/Installing/index.html. In theory, the only command needed is:

`pip install sumolib`

PS: From my experience, osmWebWizard.py (a script that will be used to generate SUMO networks) only works on the .deb version of Firefox.

## Installation / Usage

### Creating files for a new map

To create a new map, the scripts `generateMap.sh` and `generateParkingAreas.sh` are used. Maybe execution permission is needed: `chmod +x generateMap.sh` and `chmod +x generateParkingAreas.sh`.

Always execute `generateMap.sh` and then `generateParkingAreas.sh` using the same name folder.

`generateMap.sh` is going to ask for a folder name and then open a browser tab where it is possible to select the area of the map that is going to be generated. It is possible to select the area and generate the map straight away, however disabling Polygons, ignoring Aeroways, Railways and any sort of asset that is not necessary for the simulation will substantially speed up the process. More about this at https://sumo.dlr.de/docs/Tutorials/OSMWebWizard.html.

**Because of the way SUMO works, this script is not going to exit on its own, you must kill it in the terminal using `Ctrl+C` after the map is generated and the SUMO GUI is opened**. After the GUI is opened, all the files have been generated and you may close the window.

Lastly, run `generateParkingAreas.sh`to generate parking areas and rerouters for the folder you created. After this, you are all set to start creating routines for the map.

### Generating Routines and Running the Simulation

Use the command `sumo-gui osm.sumocfg` inside the map folder to start the simulation as it is using the SUMO GUI.

`pathGeneratorOSM.ipynb` is the main project notebook. It is used to generate routines for students using LLAMA (this is why you need a Groq key). Firstly, the `FOLDER_NAME` variable must be changed to the name of the desired map folder. Furthermore, to change the student information to generate the routines, it's necessary to change the `student_info` variable with the desired description. 

The routine is going to be generated based on the `places` dictionary, which should contain the names of the university institutes and tags for the other activities, these tags must exist in the OSM tags for **amenities**, **leisure** or **shop** (more about this at https://wiki.openstreetmap.org/wiki/Key:shop, https://wiki.openstreetmap.org/wiki/Category:Amenities and https://wiki.openstreetmap.org/wiki/Key:leisure). The LLM is going to generate a general routine with places like 'supermarket' or 'restaurant' and the OSM API is used to look for the closest places matching the tag.

Following this, random trips are going to be generated to fill the simulation. The `rand_trips` variable must be set to either 'None' or 'randtrips.trips.xml'. If set to None, the random trips generated will not get alternative routes (significantly faster). If set to 'randtrips.trips.xml', all the random trips will have their alternative routes calculated (significantly slower). The trips generated using the LLM are always going to have their alternative routes calculated.

To get the data from the trips generated by `pathGenerator.ipynb`, the `simulationData.ipynb` notebook is used. `vehIDs` list contains all the id's of the vehicles that are going to be tracked during the simulation, and `personIDs` for pedestrians, which is currently not supported. 

After running the simulation, the data is stored in the `veh_variables` dictionary and the `separate_plots` function may be used to plot the sensors from any of the vehicles that were tracked during the simulation.

## Citation

## Authors
  
- (2024 - today) Renan Matheus da Silva Florencio: Computer Engineering, UNICAMP
- (Advisor, 2024 - today) Paula Dornhofer Paro Costa: Professor, FEEC-UNICAMP
  
## Acknowledgements

This project is part of the Hub for Artificial Intelligence and Cognitive Architectures
(H.IAAC- Hub de Inteligência Artificial e Arquiteturas Cognitivas). Project supported by the brazilian Ministry of Science, Technology and Innovations, with resources from Law No. 8,248, of October 23, 1991.
