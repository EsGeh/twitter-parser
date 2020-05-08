FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV SHELL /bin/bash

# ------------------------------------------
# install necessary packages via apt-get:
# ------------------------------------------
# RUN apt-get update && apt-get install -y --no-install-recommends \
#   pkg1 \
#   pkg2
#   ...

# this is supposed to save memory:
# RUN rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
	postgresql-client

# this is supposed to save memory:
RUN rm -rf /var/lib/apt/lists/*

# ------------------------------------------
# install python dependencies:
# ------------------------------------------
COPY requirements.txt "$SRC_DIR/"
RUN pip install -r requirements.txt
