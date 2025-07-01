# Geliştirme aşaması
FROM node:18-alpine AS development

WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY package*.json ./
RUN npm install

# Uygulama kodunu kopyala
COPY . .


# Production build aşaması
FROM node:18-alpine AS build
WORKDIR /app

# Bağımlılıkları yükle
COPY package*.json ./
RUN npm install

# Uygulama kodunu kopyala
COPY . .

# Production build al
RUN npm run build

# Production aşaması
FROM nginx:alpine AS production

# Build aşamasından çıktıyı kopyala
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx yapılandırmasını kopyala
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 80 portunu dinle
EXPOSE 80

# Nginx'i başlat
CMD ["nginx", "-g", "daemon off;"]
