#!/usr/bin/env bash

TARGET_BRANCH="$1"
COMMIT_MSG="$2"

if [ -z "$TARGET_BRANCH" ] || [ -z "$COMMIT_MSG" ]; then
    echo "❌ Erro: Parâmetros insuficientes."
    echo "Uso: ./git_push.sh <branch> <mensagem_de_commit>"
    exit 1
fi

echo -e "\n🧹 [1/5] Corrigindo permissões de arquivos de configuração..."
# Garante que arquivos YAML e configs não fiquem com flag de executável (+x)
chmod -x odoo/custom/src/addons.yaml odoo/custom/src/repos.yaml odoo/custom/src/private/.editorconfig 2>/dev/null || true

echo -e "\n🔄 [2/5] Garantindo que estamos na branch '$TARGET_BRANCH'..."
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
    git checkout "$TARGET_BRANCH" || git checkout -b "$TARGET_BRANCH" "origin/$TARGET_BRANCH"
fi

echo -e "\n📦 [3/5] Adicionando arquivos alterados (git add .)..."
git add .

echo -e "\n📝 [4/5] Executando commit..."
git commit -m "$COMMIT_MSG"
COMMIT_STATUS=$?

# Se o pre-commit alterou arquivos e falhou a primeira tentativa de commit
if [ $COMMIT_STATUS -ne 0 ]; then
    echo -e "\n⚠️ Pre-commit aplicou formatações ou ajustes automáticos. Re-adicionando arquivos..."
    git add .
    echo "🔁 Tentando o commit novamente..."
    git commit -m "$COMMIT_MSG"
fi

echo -e "\n🚀 [5/5] Enviando alterações para o repositório remoto (git push)..."
git push origin "$TARGET_BRANCH"

if [ $? -eq 0 ]; then
    echo -e "\n✅ Processo concluído com sucesso!"
else
    echo -e "\n❌ Erro ao realizar o git push."
    exit 1
fi
