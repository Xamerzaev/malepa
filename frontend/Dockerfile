FROM node:alpine

WORKDIR /app

COPY package*.json ./
RUN yarn install

COPY . .

# Add sharp package
RUN yarn add sharp

RUN yarn build

CMD ["yarn", "start", "--", "-p", "3000"]