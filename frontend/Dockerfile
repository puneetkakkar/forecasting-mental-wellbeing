# Use an official Node.js runtime as a parent image
FROM node:14 as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY ./package*.json /app

# Install app dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . /app

# Build the Vue.js app for production
RUN npm run build

# Use a smaller, Alpine-based image of nginx as a proxy server 
# for the final container
FROM nginx:alpine

# Copy the built Vue.js app from the previous stage to place it 
# in the nginx docker file system at a particular location
# COPY --from=build /app/dist /vue-fe
COPY --from=build /app/dist /usr/share/nginx/html

# Remove the default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copying the nginx config file for serving the frontend 
# via a proxy server at a Nginx default config location
COPY ./nginx/nginx.conf /etc/nginx/conf.d

# Expose port 8080
EXPOSE 8080

# Command to run the Nginx server
CMD ["nginx", "-g", "daemon off;"]