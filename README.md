## Ukraine Agricultural Exports

Large amounts of Ukraine’s arable land are controlled by a few agribusinesses. Oakland Institute has been tracking consolidation of agricultural land as well as land reform policy in Ukraine. The goal of this application is to analyze Ukrainian agricultural exports data to see the activity of some of the companies identified in Oakland Institute's report over time.

### Installation

Software Setup
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
4. Build the Docker image: docker build -t jmacedoc1/getting-started .
5. Run the Docker image: docker run -v /path/to/output:/app/output jmacedoc1/ukraine. Where
   ```sh
   /path/to/output
   ``` is the "path" to the "output directory in your local machine.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Directory Structure
```sh
├── README.md
├── .gitignore
├── Dockerfile
├── notebooks/
│   ├── README.md
    ├── __init__.py
    ├── export_data.ipynb
    ├── land_data.ipynb
│   └── un_data_exploration.ipynb
├── utils/
│   ├── README.md
│   ├── __init__.py
│   └── python utility files
├── data/
│   ├── README.md (or SOURCES.md)
│   └── Data files
├── output/
│   ├── README.md
│   └── output images, tables, etc.
└── documentation/
    └── README.md
```




