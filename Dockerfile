# --------- Shadow Alpha API ---------
FROM python:3.11-slim AS api

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY shadow-alpha-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY shadow-alpha-api/ .
COPY shadow-alpha-quant/ /quant
RUN pip install -e /quant 2>/dev/null || true

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --------- Shadow Alpha Web ---------
FROM node:20-alpine AS web-builder

WORKDIR /app

COPY shadow-alpha-web/package*.json ./
RUN npm ci

COPY shadow-alpha-web/ .
RUN npm run build

# Production server
FROM node:20-alpine AS web

WORKDIR /app

COPY --from=web-builder /app/.next ./.next
COPY --from=web-builder /app/public ./public
COPY --from=web-builder /app/package*.json ./
COPY --from=web-builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]
