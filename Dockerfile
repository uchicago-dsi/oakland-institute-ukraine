# TODO: set up logic to handle different chip architecture using environment variables
FROM --platform=linux/arm64 osgeo/gdal:ubuntu-full-3.6.3

RUN apt-get -y update 

RUN apt -y install python3-pip libspatialindex-dev \
    && apt-get install -y --no-install-recommends \
       gdal-bin \
       libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# set a directory for the app
WORKDIR /app

# copy all the files to the container
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN mkdir -p /app/data/{ig, bsgi, panjiva, land_matrix, regional_maps}

# run the command
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
