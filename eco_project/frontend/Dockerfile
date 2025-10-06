# Use a lightweight Nginx image
FROM nginx:1.21.3-alpine

# Copy static files from the backend's static directory
COPY backend/static/*.html /usr/share/nginx/html/
COPY backend/static/*.css /usr/share/nginx/html/
COPY backend/static/*.js /usr/share/nginx/html/

# Copy Nginx config
COPY frontend/nginx.conf.template /etc/nginx/conf.d/default.conf

# Expose port 8080
EXPOSE 8080

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]