FROM python:3.8

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
