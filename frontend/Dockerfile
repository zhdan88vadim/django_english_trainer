FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY . .

# Build the app (optional - for production)
# RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
