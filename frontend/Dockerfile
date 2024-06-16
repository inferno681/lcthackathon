FROM node:22.3.0-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --prod
CMD cp -r ./dist result_build