FROM python
ENV LOGIN_FILE_PATH=/data/logins.txt
COPY ./frontend /frontend
WORKDIR /frontend
ENTRYPOINT ["python", "/frontend/frontend.py"]