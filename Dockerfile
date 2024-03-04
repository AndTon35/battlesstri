FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8051

COPY game .


CMD [ "streamlit run", "./main.py" ]