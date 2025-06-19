FROM nginx:alpine
RUN apk add --no-cache gettext
COPY index.html /usr/share/nginx/html/index.html.template
COPY nginx.conf /etc/nginx/conf.d/default.conf
CMD ["sh", "-c", "envsubst '$API_BASE' < /usr/share/nginx/html/index.html.template > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"]
