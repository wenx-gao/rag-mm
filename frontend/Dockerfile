# Nutze ein leichtes Node-Image
FROM node:22-alpine

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Paketlisten
COPY package*.json ./

# Installiere die Abhängigkeiten
RUN npm install

# Kopiere den Rest des Frontend-Codes
COPY . .

# Exponiere den Vite-Port
EXPOSE 5173

# Starte den Vite-Server mit Host-Freigabe für Docker
CMD ["npm", "run", "dev", "--", "--host"]
