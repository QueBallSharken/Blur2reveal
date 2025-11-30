FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install frontend dependencies
COPY package.json ./
RUN npm install

# Copy frontend code
COPY . .

# Expose React development server port
EXPOSE 3000

# Start React app
CMD ["npm", "start"]
