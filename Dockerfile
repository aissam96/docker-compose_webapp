FROM nginx:alpine
RUN mkdir /var/access_logs \
 && touch /var/access_logs/access.log
COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
COPY htpasswd /etc/nginx/.htpasswd
