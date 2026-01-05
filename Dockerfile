FROM python:3.12

WORKDIR /hue_light_api_control_project

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY ./app ./app

CMD ["python" , "./app/main.py"]