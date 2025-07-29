# download base image
FROM bitnami/spark:3.5.0

# Switch to root to install dependencies
USER root

# Create a directory for your app inside container
# WORKDIR /opt/spark-app

# Install Python dependencies if needed
# apt-get linux package manager
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

# Set working directory
# WORKDIR /opt/spark/work-dir

#copying requirements.txt into image

COPY opt/requirements.txt .

# # Copy your script from local machine into the container root location with a preferred name
COPY opt/spark-data/largeFileWordCount.py ./imageWordCount.py

RUN chmod +r ./*
# RUN chmod +rx ./imageWordCount.py

# Install Python requirements
RUN pip3 install -r requirements.txt

# Set environment variable for HOME to avoid the ivy error
# ENV HOME=/tmp


# Default command to run your PySpark job
CMD ["/opt/bitnami/spark/bin/spark-submit", "./imageWordCount.py"]
# TODO : 1. get the csv file
# 2: docker compose and /opt/bitnami/spark/bin/spark-submit dont need spark-submit
#3. get data back to macos so after the container dies .. response persists
