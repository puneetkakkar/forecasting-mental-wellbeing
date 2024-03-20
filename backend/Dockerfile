# Use an official Python runtime as a parent image
FROM python:3.8-slim

# # make a local directory
# RUN mkdir /backend

# set "/backend" as the working directory from which CMD, RUN, ADD references
WORKDIR /backend

# Copy the requirements file separately to leverage Docker caching
COPY requirements.txt /backend/

# pip install the local requirements.txt
RUN pip install -r requirements.txt

# now copy all the files in this directory to /backend
COPY . /backend/

# Listen to port 5000 at runtime
EXPOSE 5000

# Define our command to be run when launching the container
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:5000", "manage:app"]
