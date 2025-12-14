# climatological_data_Colombia

Personal repository of Colombian climate data for use in studies, research, and publications, always for non-commercial purposes.

Includes a Python application that allows raw data downloaded from the IDEAM hydrometeorological database to be processed into data ready for use in research.

## How to use the Python application

1. Download this repository.
2. Empty the “unprocessed_data” folder.
3. Store the raw files there in the format obtained from the IDEAM database. **Note:** Store the data for a single variable per station. If you want to process different variables from the same station, do one at a time.
4. In the root of the repository, open the Command Prompt by pressing Shift + right-click and then Open in Terminal.
5. Execute the code by typing followed by enter:
```
py library/data_processor.py
```
6. Once the algorithm is complete, you will find a single file for each station in the “data” folder with the data formatted in date and value columns. You will also find a summary in the “output” folder with the processed stations and important additional information such as the start and end dates of values, coordinates, municipality, and department of each station.

**Note:** The repository contains, as an example, raw IDEAM precipitation data from station AEROPUERTO E. CORTISSOZ - AUT [29045190].

## How to contribute

All contributions, ideas and bug reports are welcome. We encourage you to open an issue for any change or data contribution you would like to make on this project.

## Sources

1. This repository includes meteorological data downloaded from the “Consulta y Descarga de Datos Hidrometeorológicos” platform of the Instituto de Hidrología, Meteorología y Estudios Ambientale (IDEAM), which therefore owns all intellectual and industrial property rights to its data. Source: IDEAM (02/12/2025). Consulta y Descarga de Datos Hidrometeorológicos. http://dhime.ideam.gov.co/atencionciudadano/.
