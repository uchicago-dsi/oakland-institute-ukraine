# Resources:
# https://stackoverflow.com/questions/40873165/use-docker-run-command-to-pass-arguments-to-cmd-in-dockerfile
ARG ARCH

FROM --platform=linux/${ARCH} osgeo/gdal:ubuntu-full-3.6.3

RUN apt-get -y update 

RUN apt -y install python3-pip libspatialindex-dev \
    && apt-get install -y --no-install-recommends \
       gdal-bin \
       libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# set a directory for the app
WORKDIR /app

# copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install utils as a package
COPY setup.py .
COPY utils ./utils
RUN pip install -e .

ENV COUNTRY spain

# run jupyter command
CMD ["sh", "-c", "python pipeline.py ${COUNTRY}"]