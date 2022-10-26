# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app
# COPY ./app/static/ /code/app/static/
# COPY ./app/templates/ /code/app/templates/


ENV PYTHONPATH "${PYTHONPATH}:/code/app/" 
# this is necessary to use the local file

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
