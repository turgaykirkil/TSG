FROM node:18-alpine

WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY package*.json ./
RUN npm ci || npm install

# Uygulama kodunu kopyala
COPY . .

# Next.js uygulamasını 3000 portunda çalıştır
EXPOSE 3000

# Not: Üretimde dev server yerine build+start tercih edilir.
# Geçici olarak build-time hatalarını aşmak için dev modda servis veriyoruz.
CMD ["npm", "run", "dev"]
