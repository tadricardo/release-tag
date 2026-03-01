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
