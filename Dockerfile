# TODO: set up logic to handle different chip architecture using environment variables in a Makefile
# Resources:
# https://stackoverflow.com/questions/40873165/use-docker-run-command-to-pass-arguments-to-cmd-in-dockerfile

FROM --platform=linux/arm64 osgeo/gdal:ubuntu-full-3.6.3

RUN apt-get -y update 

RUN apt -y install python3-pip libspatialindex-dev \
    && apt-get install -y --no-install-recommends \
       gdal-bin \
       libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# set a directory for the app
WORKDIR /app

# copy all code besides
COPY . .

# copy requirements and install dependencies
# TODO: I guess copying this file is no longer necessary if we're already
# copying all the files with command above
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ENV COUNTRY=spain
ENV COUNTRY spain

# run jupyter command
CMD ["sh", "-c", "python pipeline.py ${COUNTRY} && jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='' --NotebookApp.password=''"]

# CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
