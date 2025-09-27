# Use a lightweight Nginx image
FROM nginx:1.21.3-alpine

# Install gettext for envsubst
RUN apk update && apk add gettext

# Copy static files
COPY *.html /usr/share/nginx/html/
COPY *.css /usr/share/nginx/html/
COPY *.js /usr/share/nginx/html/

# Copy Nginx config template
COPY nginx.conf.template /etc/nginx/conf.d/default.conf.template

# Expose port 8080
EXPOSE 8080

# Start Nginx
CMD ["/bin/sh", "-c", "envsubst < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
