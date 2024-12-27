FROM node:22.12.0-bookworm AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

ARG VITE_API_URL=${VITE_API_URL}

COPY . .

RUN npm run build

FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
