# Pets Next Door
## What my project does
My project is a web application which allows users to create posts and view posts based on location. The main theme of posts is designed to be animals or pets.

## Goal of my project
The goal of my project is to create a comfortable and lovely community where people could share stories and pictures of their pets or loved animals. 
By sharing warm stories with others, people can get closer and neighbors may know each other better, and the community will be more harmonical.

## App Screenshot
<img width="1151" alt="Screen Shot 2022-05-06 at 5 44 20 PM" src="https://user-images.githubusercontent.com/49883143/167231116-d384e415-8236-4673-acde-3be373534f01.png">

## Instruction to install(macOS)
1. Install necessary dependencies
    - `brew install postgis`
    - `brew install openssl`
    - `brew install goes`
    - `brew install proj`
2. Install PostgreSQL and PostGIS
    - Install [Docker](https://docs.docker.com/get-docker/).
    - Download [PosgreSQL/PostGIS](https://registry.hub.docker.com/r/postgis/postgis/) by running `docker pull postgis/postgis`.
3. Install `Python3.6` or above and `pip3`
4. Install GDAL(Required for Django to interface with PostGIS)
    - `pip3 install gdal`
5. Create a python virtual environment
    - In `nearbyposts` folder run `python3 -m venv env`
    - avtivate the virtual environment `source env/bin/activate`
6. Install Django and other dependencies
    - `pip3 install -r requirements.txt`

## Instuction to run server
1. Start PostgreSQL database service
    - `docker pull postgis/postgis`
    - `docker run --name nearbyposts-postgis -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=nearbyposts -d -p 5432:5432 postgis/postgis`
2. Start Django web server (Make sure the virtual environment is activated) 
    - `python3 manage.py runserver`

## References
My project is developed based on [tutorial](https://www.ashwinhariharan.tech/blog/thinking-of-building-a-contact-tracing-application-heres-what-you-can-do-instead/).

## Future extensions
Some future extensions will be login system and access control, picture uploading system and like and comment function.
