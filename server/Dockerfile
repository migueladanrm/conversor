FROM python:3.8

WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

RUN apt update && apt install ffmpeg -y

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

EXPOSE 7000

# command to run on container start
CMD [ "python", "./app.py" ]