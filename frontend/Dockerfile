# Этап сборки
FROM node:18 AS build

# Установите рабочую директорию
WORKDIR /app

# Скопируйте package.json и package-lock.json
COPY package*.json ./

# Установите зависимости
RUN npm install

# Скопируйте все файлы приложения
COPY . .

# Соберите приложение
RUN npm run build

# Этап продакшна
FROM nginx:alpine

# Скопируйте собранные файлы из предыдущего этапа
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем nginx конфигурацию (при необходимости)
# COPY nginx.conf /etc/nginx/nginx.conf

# Откройте порт
EXPOSE 80

# Запустите Nginx
CMD ["nginx", "-g", "daemon off;"]