FROM python:3.9-slim
WORKDIR /backend/
ENV TZ=Asia/Kuala_Lumpur

ENV VIRTUAL_ENV=/backend/.venv
ENV PATH=${VIRTUAL_ENV}/bin:$PATH
RUN python -m venv ${VIRTUAL_ENV}

RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    pkg-config \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python"]
CMD ["main.py"]