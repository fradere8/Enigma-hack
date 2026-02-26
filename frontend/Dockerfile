FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Запускаем в режиме разработки, открывая доступ снаружи (--host)
CMD ["npm", "run", "dev", "--", "--host"]