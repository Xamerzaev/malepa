FROM openresty/openresty:alpine-fat

RUN apk add --no-cache --virtual .run-deps \
    bash \
    curl \
    diffutils \
    mc \
    grep \
    sed \
    openssl \
    && mkdir -p /etc/resty-auto-ssl \
    && (delgroup www-data || true) \
    && addgroup -g 1000 -S www-data \
    && adduser -u 1000 -D -S -h /var/cache/nginx -s /sbin/nologin -G www-data www-data \
    && chown -R www-data:www-data /etc/resty-auto-ssl

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        libc-dev \
        make \
        openssl-dev \
        pcre-dev \
        zlib-dev \
        linux-headers \
        gnupg \
        libxslt-dev \
        gd-dev \
        geoip-dev \
        perl-dev \
        tar \
        unzip \
        zip \
        unzip \
        g++ \
        cmake \
        lua \
        lua-dev \
        make \
        autoconf \
        automake \
        build-base \
        coreutils \
        curl \
        gd-dev \
        geoip-dev \
        libxslt-dev \
        linux-headers \
        make \
        perl-dev \
        readline-dev \
        zlib-dev \
        perl-digest-md5 \
    && /usr/local/openresty/luajit/bin/luarocks install lua-resty-auto-ssl  \
    && /usr/local/openresty/luajit/bin/luarocks install lua-resty-http \
    && /usr/local/openresty/bin/opm get anjia0532/lua-resty-maxminddb \
    && apk del .build-deps \
#    && rm -rf /usr/local/openresty/nginx/conf/* \
    && mkdir -p /var/cache/nginx \
    && chown www-data -R /usr/local/openresty \
    && chgrp www-data -R /usr/local/openresty \
    && chown www-data -R /etc/resty-auto-ssl \
    && chgrp www-data -R /etc/resty-auto-ssl     
#    && ln -sf /dev/stdout /usr/local/openresty/nginx/logs/access.log \
#    && ln -sf /dev/stderr /usr/local/openresty/nginx/logs/error.log
# use self signed ssl certifacte to start nginx
RUN openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 -subj '/CN=sni-support-required-for-valid-ssl' \
        -keyout /etc/ssl/resty-auto-ssl-fallback.key \
        -out /etc/ssl/resty-auto-ssl-fallback.crt
ADD ./nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY ./ssl /etc/resty-auto-ssl