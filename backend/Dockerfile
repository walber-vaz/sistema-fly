FROM node:22.12.0-bookworm AS build

USER node

WORKDIR /usr/src/app

COPY --chown=node:node package*.json ./

RUN npm ci

COPY --chown=node:node . .

RUN npm run build \
    && rm -rf node_modules \
    && npm cache clean --force

ENV NODE_ENV=production

RUN npm ci --omit=dev \
    && npm cache clean --force

FROM node:22.12.0-alpine3.21

USER node

WORKDIR /usr/src/app

COPY --chown=node:node --from=build /usr/src/app/node_modules ./node_modules
COPY --chown=node:node --from=build /usr/src/app/dist ./dist

EXPOSE 3000

CMD ["node", "dist/main.js"]
