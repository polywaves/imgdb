FROM nginx:alpine

RUN rm -rf /etc/nginx/conf.d 
RUN rm /etc/nginx/nginx.conf

COPY ./conf.d/ /etc/nginx/conf.d/
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./ssl/ /etc/nginx/ssl/
RUN chmod 600 /etc/nginx/ssl/*.key

WORKDIR /var/www/html