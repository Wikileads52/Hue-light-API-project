FROM python:3.12-slim

WORKDIR /hue_light_api_control_project

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY ./app ./app

CMD ["python" , "./app/main.py"]