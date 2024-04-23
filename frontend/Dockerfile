FROM python:3.9-slim
WORKDIR /frontend/
ENV TZ=Asia/Kuala_Lumpur

ENV VIRTUAL_ENV=/frontend/.venv
ENV PATH=${VIRTUAL_ENV}/.local/bin:$PATH
RUN python -m venv ${VIRTUAL_ENV}

RUN apt-get update && \
    apt-get install -y cron && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /frontend/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /frontend/

# Due to the summer time for U.S. stock market, the market is closed at 4am. 
RUN echo "0 4 * * * cd /frontend && ${VIRTUAL_ENV}/bin/python schedule_requests.py >> /var/log/cron.log 2>&1" | crontab -

RUN echo '#!/bin/bash\n\
cron\n\
streamlit run Home.py\n\
' > /frontend/entrypoint.sh && \
    chmod +x /frontend/entrypoint.sh

ENTRYPOINT ["/frontend/entrypoint.sh"]
CMD []
