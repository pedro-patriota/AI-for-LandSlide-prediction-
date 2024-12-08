# GeoSafe

## Description
GeoSafe is project which aims to predict landslides occurrences in urban areas of Recife, Brazil. This is done by analyzing emergency calls data together with climate and geological data. We use clustering algorithms to map different patterns of landslides and measure how close a point in time is to a pattern.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## Installation
Installation is done by downloading the required Python libraries and inserting API KEY from Google Maps Geocode application.
````aiignore
export $API_KEY={Google Maps API Key}
````

```bash
pip install -r requirements.txt 
```

## Usage
In the current state, GeoSafe does not have automatic script files and thus is needed to run each file individually. 
#### Processing
The processing follows this structure:
```python
python processing/remove_column/remove.py
```
```python
python processing/merge/merge_tables.py
```
```python
python processing/location/get_latitude_longitude.py
```
```python
python processing/ground_type/get_ground_type.py
```
```python
python processing/ground_amplitude/get_ground_amplitude.py
```
```python
python processing/danger_level/get_danger_level.py
```
```python
python processing/rain_elevation/get_rain_elevation.py
```
```python
python processing/setup_algorithm/setup_algorithm.py
```

#### Algorithm
We currently use K means and HBSCAN for clustering algorithms after processing, you may run each file independently. Their results will be stored in the .ipynb file and in .csv 

## Contributing
For now, the main source of data is Civil Defense of Recife emergency calls, through this dataset:
http://dados.recife.pe.gov.br/dataset/monitoramento-das-areas-de-riscos/resource/5eaed1e8-aa7f-48d7-9512-638f80874870?inner_span=True

Other sources include:
- Public Ground data from EMBRAPA(https://www.embrapa.br)
- Public Danger level data from CEMADEN(https://www.gov.br/cemaden/pt-br)
- Public Climate data from INMEP(https://portal.inmet.gov.br)

You may contribute by adding new sources of data and improving the current use of these databases. And, of course, working on the clustering algorithms to improve performance and precision. 

## Contact
Pedro Patriota - pasp@cin.ufpe.br
