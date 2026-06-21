FROM python:3.12-slim

ENV TZ=Europe/Lisbon

WORKDIR /app

COPY watering_system_controller.py /app/
COPY run.sh /run.sh

RUN pip install --no-cache-dir paho-mqtt \
    && chmod +x /run.sh

CMD ["/run.sh"]