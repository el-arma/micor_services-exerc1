# Use a lightweight Node.js image
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json files (if present)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the remaining source files
COPY . .

# Expose port 3000
EXPOSE 3000

# Start command
CMD ["npm", "start"]

# to Build:
    # docker build -t recommendation-service .

# to Run:
    # docker run -d -p 5432:5432 --name lunchbox-db lunchbox-postgres