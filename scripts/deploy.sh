#!/usr/bin/env bash

set -e
set -u
set -o pipefail

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log "Erro: Docker não está rodando. Por favor, inicie o serviço Docker."
        exit 1
    fi
}

check_compose_files() {
    if [ ! -f "docker-compose-prod.yml" ]; then
        log "Erro: arquivo docker-compose-prod.yml não encontrado"
        exit 1
    fi
}

log "Iniciando verificações de pré-requisitos..."
check_docker
check_compose_files

log "Iniciando deploy dos serviços principais..."
if ! docker compose -f docker-compose-prod.yml up -d --build --force-recreate; then
    log "Erro ao fazer deploy dos serviços principais"
    exit 1
fi

log "Realizando limpeza de imagens não utilizadas..."
docker image prune -f

log "Deploy concluído com sucesso!"