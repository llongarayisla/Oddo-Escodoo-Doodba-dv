#!/usr/bin/env bash

TARGET_BRANCH="$1"
COMMIT_MSG="$2"

if [ -z "$TARGET_BRANCH" ] || [ -z "$COMMIT_MSG" ]; then
    echo "❌ Erro: Parâmetros insuficientes."
    exit 1
fi

echo -e "\n🧹 [1/5] Corrigindo permissões de arquivos de configuração..."
chmod -x odoo/custom/src/addons.yaml odoo/custom/src/repos.yaml odoo/custom/src/private/.editorconfig 2>/dev/null || true

echo -e "\n🔄 [2/5] Garantindo que estamos na branch '$TARGET_BRANCH'..."
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
    git checkout "$TARGET_BRANCH" || git checkout -b "$TARGET_BRANCH" "origin/$TARGET_BRANCH"
fi

echo -e "\n📦 [3/5] Adicionando arquivos alterados (git add .)..."
git add .

# Verifica se existem alterações staged para commit
if git diff --staged --quiet; then
    echo -e "\n⚠️ Nenhuma alteração pendente encontrada para commit."
    echo "Tudo limpo no repositório."
    exit 0
fi

echo -e "\n📝 [4/5] Executando commit..."
git commit -m "$COMMIT_MSG"
COMMIT_STATUS=$?

# Tratamento do Pre-commit (Ajustes automáticos vs Erros reais)
if [ $COMMIT_STATUS -ne 0 ]; then
    echo -e "\n⚠️ Pre-commit aplicou formatações ou falhou na verificação."
    echo "Re-adicionando arquivos e tentando novamente..."
    git add .
    git commit -m "$COMMIT_MSG"

    if [ $? -ne 0 ]; then
        echo -e "\n❌ Falha persistente no pre-commit (Erros no código ou linting)."
        exit 4
    fi
fi

echo -e "\n🚀 [5/5] Enviando alterações para o repositório remoto (git push)..."
git push origin "$TARGET_BRANCH"
PUSH_STATUS=$?

if [ $PUSH_STATUS -ne 0 ]; then
    # Diagnóstico preliminar de erros de Push
    if git status | grep -q "ahead"; then
        echo -e "\n❌ Erro de Push: Mudanças remotas pendentes de Pull."
        exit 2
    elif git status | grep -q "Unmerged"; then
        echo -e "\n❌ Erro de Push: Conflitos não resolvidos."
        exit 3
    else
        echo -e "\n❌ Erro desconhecido durante o git push."
        exit 1
    fi
fi

echo -e "\n✅ Processo concluído com sucesso!"
exit 0
