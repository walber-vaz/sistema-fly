FROM node:20.18.1-bookworm AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install -g npm@11.0.0 \
    && npm install

COPY . ./

ARG VITE_API_URL=${VITE_API_URL}

RUN npm run build

FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
