FROM python:2
RUN mkdir /var/error_log \
 && touch /var/error_log/error.log
ADD script.py /
RUN chmod 755 ./script.py
CMD [ "python", "-u", "./script.py" ]