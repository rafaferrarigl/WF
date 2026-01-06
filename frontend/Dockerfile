FROM node:24.12 AS builder

WORKDIR /build


COPY package*.json ./
RUN npm install


COPY angular.json ./
COPY tsconfig*.json ./

COPY src src
RUN npm run build



FROM caddy:2.10.2-alpine AS runner

WORKDIR /app


COPY security security
COPY public ./www/public
COPY --from=builder /build/dist/frontend/browser ./www
COPY Caddyfile /etc/caddy/Caddyfile


CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]


EXPOSE 443
