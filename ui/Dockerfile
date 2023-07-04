# Use a lightweight base image
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the nginx.conf file to the appropriate location
COPY nginx.conf /etc/nginx/nginx.conf

# Create a directory to store the Hebrew fonts
RUN mkdir -p /usr/share/nginx/html/fonts

# Copy the Hebrew font files to the fonts directory
COPY fonts/* /usr/share/nginx/html/fonts/

# Copy your index.html file to the nginx html directory
COPY index.html /usr/share/nginx/html/

COPY img /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]

