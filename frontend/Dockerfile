FROM node:22.12.0-bookworm AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

ARG VITE_API_URL=${VITE_API_URL}

COPY . ./

RUN npm run build

FROM nginx:stable-alpine as production-stage

COPY nginx/nginx.conf /etc/nginx/

RUN apk update && apk upgrade \
    && apk --update add logrotate openssl bash \
    && apk add --no-cache certbot certbot-nginx \
    && rm -rf /var/cache/apk/*

RUN rm -rf /etc/nginx/conf.d/default.conf

RUN adduser -D -H -u 1000 -s /bin/bash www-data -G www-data

RUN mkdir -p /var/www \
    && chown -R www-data:www-data /var/www \
    && chmod 755 -R /var/www

RUN mkdir -p /etc/nginx/site-available /etc/nginx/conf.d /var/www/sistemafly \
    && chown -R www-data:www-data /etc/nginx/site-available /etc/nginx/conf.d /var/www/sistemafly

COPY --from=build-stage /app/dist /var/www/sistemafly

RUN apk del --no-cache

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
