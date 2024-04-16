FROM python:3.9-slim
WORKDIR /frontend/
ENV TZ=Asia/Kuala_Lumpur

ENV VIRTUAL_ENV=/frontend/.venv
ENV PATH=${VIRTUAL_ENV}/.local/bin:$PATH
RUN python -m venv ${VIRTUAL_ENV}

COPY requirements.txt /frontend/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["streamlit", "run"]
CMD ["webapp.py"]