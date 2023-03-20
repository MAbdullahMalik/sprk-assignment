FROM python:3.8
# RUN mkdir build
# WORKDIR /build
# COPY . .

RUN pip install pipenv
WORKDIR /src/
COPY Pipfile  /src/Pipfile
COPY Pipfile.lock /src/Pipfile.lock
COPY requirements.txt /src/requirements.txt
RUN pipenv install
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src/ /src/
CMD python -m uvicorn app:app --host 0.0.0.0 --port 8000
