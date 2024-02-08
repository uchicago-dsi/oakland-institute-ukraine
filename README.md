## Ukraine Agricultural Exports

Large amounts of Ukraine’s arable land are controlled by a few agribusinesses. Oakland Institute has been tracking consolidation of agricultural land as well as land reform policy in Ukraine. The goal of this application is to analyze Ukrainian agricultural exports data to see the activity of some of the companies identified in Oakland Institute's report over time: [https://www.oaklandinstitute.org/war-theft-takeover-ukraine-agricultural-land](https://www.oaklandinstitute.org/war-theft-takeover-ukraine-agricultural-land)

### Installation

This setup should only have to be run once per machine you run it on.

1. Install Docker. The project is designed to run in a Docker container. Therefore, the only prerequisite is Docker: [Get Docker](https://docs.docker.com/get-docker/)
2. Clone the repo
   ```sh
   git clone https://github.com/uchicago-dsi/oakland-institute-ukraine.git
   ```
3. Change to the root project directory:
   ```sh
   cd oakland-institute-ukraine
   ```
4. Switch to the `dev` branch.
5. Dowload `ig` folder data files [here](https://drive.google.com/drive/folders/1OPAzWTEhAXpetQs9hApin_KW1GmGRpf4).
7. Create a `data` directory and move the downloaded data files (`ig` directory) from the previous step to the `data` directory you just created with something similar to the following commands:
   ```sh
   mkdir data
   mv path/to/downloaded_data/ig path/to/repo/data/ig 
   ```

TODO: need to add instructions for .env file and Make commands

6. Build the Docker image from the root project directory:
   ```sh
   docker build -t ukraine .
   ```
7. TODO: Set this up as a Make command
   TODO: need to mount the data directory as a volume
   TODO: add a Docker bash command to the Makefile
   Run the Docker image:

   ```sh
   docker run -v $(pwd)/notebooks:/app/notebooks -v $(pwd)/data:/app/data --name notebooks-jupyter --rm -p 8888:8888 -t ukraine
   ```

   This works:
   `docker run -v $(pwd)/notebooks:/app/notebooks --rm -it ukraine /bin/bash`
   Where `$(current_abs_path)` is the path to the repo directory in your local machine.

8. Copy and paste the Jupyter server URL in your preferred web browser.
9. Go to the `\notebooks` directory and open each notebook.

### Data files

`/bsgi`

`bsgi_destinations.csv`: Black Sea Grain Initiative dataset with volume of exports
data ("total metric tons" column) grouped by country of destination ("Country" column).
Data corresponds to three Black Sea ports: Odesa, Chornomorsk, Yuzhny/Pivdennyi.<br>
`bsgi_outbound.csv`: Black Sea Grain Initiative dataset with exports
data disaggregated at the shipment level. Data corresponds to three Black Sea
ports: Odesa, Chornomorsk, Yuzhny/Pivdennyi.

`/ig`

`ig_kernel_10000.csv`: Import Genius data containing information on shipment exports for Kernel
(company in top 10 firms controlling agricultural land in Ukraine).

`/land_matrix`

`deals.csv`: Land Matrix data on land deals around the world at the "Company" level.
It also has information about the "Target country" of the land deal.<br>
`locations.csv`: Land Matrix data on land deals locations with coordinates ("Point" column).
It seems that locations are at disaggregated at least at the "hromada" level (municipal level).

`/panjiva`

Excel files with export data from Panjiva for the top 10 firms controlling
agricultural land in Ukraine and its subsidiaries. Files are named following the
syntax "panjiva\_[companya_name].xlsx".

`/regional_maps`

`ukr_admbnda_adm3_sspe_20230201.shp`: shape file from The Humanitarian Data Exchange
project with Ukrainian administrative divisions at the 3rd level of disaggregation.
We believe it is the "hromada" or municipality level but we cannot confirm from
the available documentation: [https://data.humdata.org/dataset/cod-ab-ukr](https://data.humdata.org/dataset/cod-ab-ukr)

### Directory Structure

```sh
.
├── .gitignore
├── Dockerfile
├── README.md
├── __init__.py
├── requirements.txt
├── notebooks/
│   ├── README.md
│   ├── __init__.py
│   ├── export_data.ipynb
│   ├── land_data.ipynb
│   ├── panjiva.ipynb
│   └── un_data_exploration.ipynb
├── output/
│   └── README.md
└── utils/
    ├── README.md
    ├── __init__.py
    ├── app.py
    ├── clean_data.py
    ├── get_data.py
    ├── map.py
    ├── plot.py
    ├── record_linkage.py
    └── transform_data.py
```
