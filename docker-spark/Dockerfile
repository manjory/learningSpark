FROM bitnami/spark:latest

# Create a directory for your app inside container
WORKDIR /opt/spark-app

# Copy your script from local machine into the container
COPY largeFileWordCount.py /opt/spark-app/

# Make sure permissions are okay (optional)
RUN chmod +x /opt/spark-app/largeFileWordCount.py

# Set environment variable for HOME to avoid the ivy error
ENV HOME=/tmp

# Run spark-submit on your script by default (you can override this command)
CMD ["/opt/bitnami/spark/bin/spark-submit", "/opt/spark-app/largeFileWordCount.py"]
