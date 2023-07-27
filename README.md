## Ukraine Agricultural Exports

Large amounts of Ukraine’s arable land are controlled by a few agribusinesses. Oakland Institute has been tracking consolidation of agricultural land as well as land reform policy in Ukraine. The goal of this application is to analyze Ukrainian agricultural exports data to see the activity of some of the companies identified in Oakland Institute's report over time.

### Installation

Software Setup
This setup should only have to be run once per machine you run it on.

1. Install Docker. The project is designed to run in a Docker container. Therefore, the only prerequisite is Docker: [Get Docker](https://docs.docker.com/get-docker/)
2. Dowload data files: [https://drive.google.com/drive/folders/1juoPDrmR-2--zAKIpj8LP2NAnkgqVsTL](https://drive.google.com/drive/folders/1juoPDrmR-2--zAKIpj8LP2NAnkgqVsTL)
3. Clone the repo
   ```sh
   git clone https://github.com/uchicago-dsi/oakland-institute-ukraine.git
   ```
4. Change to the root project directory:
   ```sh
   cd oakland-institute-ukraine
   ```
5. Create a ```/data``` directory and move the downloaded data files to the "/data" directory.
5. Build the Docker image from the root project directory:
   ```sh
   docker build -t ukraine .
   ```
6. Run the Docker image:
   ```sh
   docker run -v $(current_abs_path):/notebooks --name notebooks-jupyter --rm -p 8888:8888 -t ukraine
   ```
   
   Where
   ```sh
   $(current_abs_path)
   ```
   is the path to the repo directory in your local machine.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Directory Structure

```sh
.
├── README.md
├── .gitignore
├── Dockerfile
├── __init__.py
├── app.py
├── requirements.txt
├── notebooks/
│   ├── README.md
│   ├── __init__.py
│   ├── export_data.ipynb
│   ├── land_data.ipynb
│   └── un_data_exploration.ipynb
├── output/
│   └── README.md
├── utils/
│   ├── README.md
│   ├── __init__.py
│   ├── clean_data.py
│   ├── get_data.py
│   ├── plot.py
│   └── record_linkage.py
└── documentation/
    └── README.md
```
