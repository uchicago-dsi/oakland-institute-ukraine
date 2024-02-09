## Ukraine Agricultural Exports

Large amounts of Ukraine’s arable land are controlled by a few agribusinesses. Oakland Institute has been tracking consolidation of agricultural land as well as land reform policy in Ukraine. The goal of this application is to analyze Ukrainian agricultural exports data to see the activity of some of the companies identified in Oakland Institute's report over time: [https://www.oaklandinstitute.org/war-theft-takeover-ukraine-agricultural-land](https://www.oaklandinstitute.org/war-theft-takeover-ukraine-agricultural-land)

We are interested in the export shares of some Ukrainian companies to other countries and regions. The following code will help analyze export shares to the specified country or region: Spain, Belgium or Asia.

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
5. Dowload all data files [here](https://drive.google.com/drive/folders/1juoPDrmR-2--zAKIpj8LP2NAnkgqVsTL).
6. Unzip the downloaded `.zip` file and move the `data` folder from the previous step to a `data` directory in your root project directory with something like:
   ```sh
   mv path/to/downloaded_data path/to/repo/data
   ```
7. Create an `.env` file in the root directory and set the `COUNTRY` variable to the country/region you want to analyze: "spain", "belgium" or "asia". The `.env`file should look like this:
   ```sh
   COUNTRY="country"
   ```
8. Open Docker Desktop (in case it wasn't running already) and build the Docker image from the root project directory with the following command:
   ```sh
   make build
   ```
9. If you want to re-run the data pipeline (i.e. clean the data files) run the following command:
   ```sh
   make run-pipeline
   ```
   
   You can check the clean data files at the `data/ig/` directory named as "ig_clean_<country>".

10. If you want to see the data visualizations for the corresponding country in a Jupyter notebook without re-running the data pipeline run:
   ```sh
   make jupyter
   ```

   a. Copy and paste the Jupyter server URL in your preferred web browser.\
   b. Open the `exports_shares.ipynb` file and add the set the `country` variable to the corresponding country.
   c. Run the notebook and see the visualizations.
 

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
