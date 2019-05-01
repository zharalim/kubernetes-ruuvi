FROM python:3-slim

WORKDIR /opt/ruuvi

RUN apt-get update && \
    apt-get -y install python3-dev python3-psutil && \
    apt-get -y install bluez bluez-hcidump && \
    apt-get clean

COPY requirements.txt ./
# ruuvitag lib requires sudo when running
RUN apt-get update && \
    apt-get -y install gcc sudo && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get -y remove gcc && \
    apt -y autoremove && \
    apt-get clean

COPY ruuvi.py ./

CMD [ "python", "./ruuvi.py" ]
