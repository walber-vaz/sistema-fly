#!/usr/bin/env bash

# Habilita modo estrito de execução
set -e  # Interrompe o script se algum comando falhar
set -u  # Trata variáveis não definidas como erro
set -o pipefail  # Faz os pipes retornarem erro se algum comando falhar

# Função para exibir mensagens de log com timestamp
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Função para verificar se o Docker está rodando
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log "Erro: Docker não está rodando. Por favor, inicie o serviço Docker."
        exit 1
    fi
}

# Função para verificar se o docker-compose está instalado
check_docker_compose() {
    if ! command -v docker-compose >/dev/null 2>&1; then
        log "Erro: docker-compose não está instalado."
        exit 1
    fi
}

# Função para verificar se os arquivos docker-compose existem
check_compose_files() {
    if [ ! -f "docker-compose-traefik.yml" ]; then
        log "Erro: arquivo docker-compose-traefik.yml não encontrado"
        exit 1
    fi
    if [ ! -f "docker-compose-prod.yml" ]; then
        log "Erro: arquivo docker-compose-prod.yml não encontrado"
        exit 1
    fi
}

# Executa verificações iniciais
log "Iniciando verificações de pré-requisitos..."
check_docker
check_docker_compose
check_compose_files

# Criar rede se não existir
if ! docker network ls | grep -q net_sistema_fly; then
    log "Criando rede net_sistema_fly..."
    docker network create net_sistema_fly
    log "Rede criada com sucesso"
fi

# Gerenciar Traefik
if ! docker ps | grep -q traefik; then
    log "Iniciando Traefik pela primeira vez..."
    if ! docker compose -f docker-compose-traefik.yml up -d; then
        log "Erro ao iniciar Traefik"
        exit 1
    fi
    log "Aguardando inicialização do Traefik (30s)..."
    sleep 30
else
    log "Atualizando Traefik..."
    if ! docker compose -f docker-compose-traefik.yml up -d --force-recreate; then
        log "Erro ao atualizar Traefik"
        exit 1
    fi
fi

log "Aguardando estabilização do Traefik (10s)..."
sleep 10

# Deploy dos serviços principais
log "Iniciando deploy dos serviços principais..."
if ! docker compose -f docker-compose-prod.yml up -d --build --force-recreate; then
    log "Erro ao fazer deploy dos serviços principais"
    exit 1
fi

# Limpeza de imagens
log "Realizando limpeza de imagens não utilizadas..."
docker image prune -f

log "Deploy concluído com sucesso!"