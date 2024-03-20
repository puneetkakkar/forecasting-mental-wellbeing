FROM nginx:alpine

# Remove the current default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy the new nginx config to nginx container's folder
COPY ./nginx.conf /etc/nginx/conf.d