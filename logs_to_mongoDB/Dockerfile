FROM python:2
RUN mkdir /var/access_logs \
 && touch /var/access_logs/access.log
ADD script.py /
RUN python -m pip install pymongo \
    && pip install watchdog \
    && chmod 755 ./script.py
CMD [ "python", "-u", "./script.py" ]

