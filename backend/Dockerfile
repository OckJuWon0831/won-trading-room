FROM python:3.9-slim
WORKDIR /backend/
ENV TZ=Asia/Kuala_Lumpur

ENV VIRTUAL_ENV=/backend/.venv
ENV PATH=${VIRTUAL_ENV}/bin:$PATH
RUN python -m venv ${VIRTUAL_ENV}

COPY requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["python"]
CMD ["main.py"]