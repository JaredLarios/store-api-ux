FROM python:3.12

# Copy the application into the container.
COPY . /code

# Install the application dependencies.
WORKDIR /code

# Install libraries
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8090"]