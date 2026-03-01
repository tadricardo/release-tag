# release-tag

pip install python-semantic-release

git commit -m "feat: init app"
git commit -m "fix: correction d'un bug sur l'IHM"
git commit -m "feat!: changement de BDD MySQL to MariaDB"

| Type                    | Impact sur la version                                               |
| ----------------------- | ------------------------------------------------------------------- |
| **feat:**               | nouvelle fonctionnalité → **MINOR**                                 |
| **fix:**                | correction de bug → **PATCH**                                       |
| **feat!:** ou **fix!:** | breaking change → **MAJOR**                                         |
| **chore:**              | maintenance, refactor, mise à jour dépendances → **aucune version** |
| **docs:**               | documentation → **aucune version**                                  |
| **test:**               | tests → **aucune version**                                          |

commande de test: python-semantic-release version

# exporter ton token Personal access token qui est associé au GH_TOKEN de la CI/CD

- **set GH_TOKEN=ton_token_ici** ou **export GH_TOKEN=ton_token_ici** pour (Linux/macOS)

# Commande mettre à jour le fichier CHANGELOG.md en local

- semantic-release changelog

# Mis en place du pre-commit

- pip install pre-commit
- pre-commit sample-config > .pre-commit-config.yaml
- pre-commit install
