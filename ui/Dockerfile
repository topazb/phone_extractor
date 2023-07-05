# Use a lightweight base image
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the nginx.conf file to the appropriate location
#COPY nginx.conf /etc/nginx/nginx.conf

COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]
