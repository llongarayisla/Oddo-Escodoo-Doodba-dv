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


def main():
    print("=" * 60)
    print(" 🚀 Odoo-Escudo Git Commit & Push Helper")
    print("=" * 60)

    current_branch, branches = get_git_branches()

    if not branches:
        print("❌ Erro: Não foi possível identificar branches no repositório Git.")
        sys.exit(1)

    print(f"\n📌 Branch atual: \033[1;32m{current_branch}\033[0m\n")
    print("Branches disponíveis no repositório:")
    for idx, branch in enumerate(branches, 1):
        marker = " (atual)" if branch == current_branch else ""
        print(f"  [{idx}] {branch}{marker}")

    selected_branch = current_branch
    choice = input(
        f"\nEscolha o número da branch para Push [Padrão: {current_branch}]: "
    ).strip()
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

    commit_msg = input("✍️  Digite a mensagem de commit: ").strip()
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
        subprocess.run(cmd, check=True)
    else:
        print("❌ Operação cancelada pelo usuário.")


if __name__ == "__main__":
    main()
