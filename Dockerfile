FROM python:3.7
ENV PYTHONUNBUFFERED 0
RUN pip3 install --upgrade pip
COPY shelter /app/shelter
COPY setup.py /app
WORKDIR app
RUN pip3 install .
ENTRYPOINT api
