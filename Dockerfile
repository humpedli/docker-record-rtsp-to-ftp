FROM python:3-stretch

# copy files
COPY . /usr/src/app

# set workdir
WORKDIR /usr/src/app

# install dependencies
RUN apt-get update && apt-get -y dist-upgrade && \
	apt-get -y install ffmpeg libav-tools

# cleanup
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*

# entry point
CMD python script.py 11122

# expose port
EXPOSE 11122