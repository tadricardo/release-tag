# release-tag

pip install python-semantic-release

git commit -m "feat: init app"
git commit -m "fix: correction d'un bug sur l'IHM"
git commit -m "feat!: changement de BDD MySQL to MariaDB"

| Type  | Impact |
| ----- | ------ |
| fix   | PATCH  |
| feat  | MINOR  |
| feat! | MAJOR  |

commande de test: python-semantic-release version --dry-run -vv
