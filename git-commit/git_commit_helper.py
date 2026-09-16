#!/usr/bin/env python3
# pylint: disable=print-used,W8116
import subprocess
import sys


def run_cmd(cmd):
    """Executa um comando no terminal e retorna a saída formatada."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def get_git_branches():
    """Obtém a lista de branches locais e remotas."""
    run_cmd("git fetch --all --prune")
    current_branch = run_cmd("git branch --show-current")
    raw_branches = run_cmd("git branch -a --format='%(refname:short)'")
    branches = []

    for b in raw_branches.split("\n"):
        b = b.strip()
        if not b:
            continue
        if b.startswith("origin/"):
            b = b.replace("origin/", "")
        if b not in branches and b != "HEAD":
            branches.append(b)

    return current_branch, branches


def diagnose_git_error(returncode):
    """Diagnostica falhas comuns do Git/Pre-commit e orienta o usuário."""
    print("\n" + "x" * 60)
    print(" ⚠️ DIAGNÓSTICO DE FALHA DO GIT / PRE-COMMIT")
    print("x" * 60)

    if returncode == 2:
        print(
            "🔍 Motivo: O repositório remoto contém alterações "
            "que você não tem localmente."
        )
        print("💡 Como resolver:")
        print("   Execute no terminal: git pull --rebase origin <branch>")
    elif returncode == 3:
        print("🔍 Motivo: Conflito de mesclagem (Merge Conflict).")
        print("💡 Como resolver:")
        print("   1. Resolva os conflitos nos arquivos indicados.")
        print("   2. Execute: git add .")
        print("   3. Rode o assistente novamente.")
    elif returncode == 4:
        print(
            "🔍 Motivo: O pre-commit bloqueou por erros não corrigíveis "
            "automaticamente."
        )
        print("💡 Como resolver:")
        print("   Verifique as mensagens do linter (Ruff/Pylint/ESLint).")
        print("   Corrija o código no seu editor e tente novamente.")
    else:
        print("🔍 Motivo: Erro genérico durante a execução do comando Git.")
        print("💡 Verifique o histórico de logs acima para entender a falha.")
    print("x" * 60 + "\n")


def process_commit():
    """Executa um ciclo completo de escolha, commit e push."""
    print("\n" + "=" * 60)
    print(" 🚀 Odoo-Escudo Git Commit & Push Helper")
    print("=" * 60)

    current_branch, branches = get_git_branches()

    if not branches:
        print("❌ Erro: Não foi possível identificar branches no repositório.")
        return

    print(f"\n📌 Branch atual: \033[1;32m{current_branch}\033[0m\n")
    print("Branches disponíveis no repositório:")
    print("  [0] Sair do assistente")
    for idx, branch in enumerate(branches, 1):
        marker = " (atual)" if branch == current_branch else ""
        print(f"  [{idx}] {branch}{marker}")

    selected_branch = current_branch
    prompt_msg = f"\nEscolha a branch para Push [Padrão: {current_branch} | 0 sair]: "
    choice = input(prompt_msg).strip()

    if choice in ["0", "q", "quit", "exit"]:
        print("👋 Encerrando o assistente...")
        sys.exit(0)

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(branches):
            selected_branch = branches[idx]

    print("\n" + "-" * 60)
    print("Tipos comuns de commit (Conventional Commits):")
    print("  feat(escopo): Nova funcionalidade")
    print("  fix(escopo): Correção de bug")
    print("  docs(escopo): Atualização de documentação")
    print("  refactor(escopo): Refatoração de código sem alterar regra")
    print("-" * 60)

    commit_msg = input(
        "✍️  Digite a mensagem de commit (ou 'c' para cancelar): "
    ).strip()
    if commit_msg.lower() in ["c", "cancelar"]:
        print("🔄 Operação cancelada. Retornando ao menu principal...")
        return

    while not commit_msg:
        print("⚠️ A mensagem de commit não pode ser vazia.")
        commit_msg = input("✍️  Digite a mensagem de commit: ").strip()

    print("\n" + "=" * 60)
    print(f"🎯 Target Branch: {selected_branch}")
    print(f"💬 Commit Msg   : {commit_msg}")
    print("=" * 60)

    confirm = input("Deseja prosseguir? [S/n]: ").strip().lower()
    if confirm in ["", "s", "sim", "y", "yes"]:
        cmd = [
            "bash",
            "./git-commit/git_push.sh",
            selected_branch,
            commit_msg,
        ]

        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            diagnose_git_error(result.returncode)
    else:
        print("🔄 Operação cancelada pelo usuário.")


def main():
    """Loop principal para manter o script rodando de forma contínua."""
    while True:
        try:
            process_commit()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Operação interrompida pelo usuário. Encerrando...")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erro crítico no código do assistente: {e}")
            print(
                "💡 Por favor, verifique o script Python " "'git_commit_helper.py'.\n"
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
