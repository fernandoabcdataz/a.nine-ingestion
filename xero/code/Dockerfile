FROM python:3.9-slim

# set the working directory in the container
WORKDIR /app

# copy the current directory contents into the container at /app
COPY . /app

# install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# make port 8080 available to the world outside this container
EXPOSE 8080

# define environment variable
ENV PORT=8080

# run main.py when the container launches
CMD ["python", "main.py"]