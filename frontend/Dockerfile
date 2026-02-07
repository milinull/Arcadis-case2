# Node
FROM node:18-alpine

WORKDIR /app

# Copia arquivos de dependência
COPY package*.json ./

# Instala as dependências ignorando conflitos de peer
RUN npm install --legacy-peer-deps

# Copia o restante do código
COPY . .

# Expõe a porta que o React utiliza
EXPOSE 3001

# Comando para iniciar o app em modo desenvolvimento
CMD ["npm", "start"]