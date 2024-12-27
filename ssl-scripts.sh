#!/bin/bash

# Configurações
domain="sistemafly.wssoftwares.com.br"
email="wvs.walber@gmail.com"
data_path="./certbot"

# Criar diretórios
mkdir -p "$data_path/conf/live/$domain"
mkdir -p "$data_path/www"

# Limpar configurações antigas
rm -rf "$data_path/conf/*"
rm -rf "$data_path/www/*"

# Parar containers existentes
docker compose -f docker-compose-prod.yml down

# Iniciar nginx sem SSL primeiro
cat > nginx.conf << 'EOF'
server {
    listen 80;
    server_name sistemafly.wssoftwares.com.br;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files $uri =404;
    }

    location / {
        return 200 'Ok';
    }
}
EOF

# Iniciar nginx
docker compose -f docker-compose-prod.yml up -d nginx

# Aguardar nginx iniciar
sleep 10

# Tentar obter certificado
docker compose -f docker-compose-prod.yml run --rm --entrypoint "\
    certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    --email $email \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    --debug-challenges \
    -v \
    -d $domain" \
    certbot

# Verificar se obteve o certificado
if [ -f "$data_path/conf/live/$domain/fullchain.pem" ]; then
    echo "Certificado obtido com sucesso!"
    # Restaurar configuração nginx completa
    cp nginx.conf.original nginx.conf
else
    echo "Falha ao obter certificado"
    echo "Verifique:"
    echo "1. DNS está configurado corretamente"
    echo "2. Porta 80 está aberta"
    echo "3. Se está usando Cloudflare, desative o proxy temporariamente"
fi

# Reiniciar nginx
docker compose -f docker-compose-prod.yml exec nginx nginx -s reload