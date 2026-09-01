# Epic Events CRM

CRM en ligne de commande pour Epic Events : gestion des clients, contrats et
evenements, avec permissions par role (commercial / gestion / support) et
journalisation des erreurs via Sentry.

## Prerequis

- Python 3.9 ou plus recent
- Un serveur MySQL accessible

## Installation

```bash
git clone <url-du-repo>
cd crm

python -m venv env
# Windows
env\Scripts\activate
# macOS / Linux
source env/bin/activate

pip install -r requirements.txt
```

## Configuration (.env)

Copier `.env.example` en `.env` puis renseigner les valeurs :

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | Chaine de connexion MySQL, ex: `mysql+pymysql://USER:PASSWORD@localhost:3306/DATABASE` |
| `SECRET_KEY` | Cle secrete servant a signer les tokens de session CLI (JWT). A generer avec `python -c "import secrets; print(secrets.token_hex(32))"` |
| `SENTRY_DSN` | DSN du projet Sentry (Python) utilise pour la journalisation. Laisser vide pour desactiver Sentry (utile en local/tests) |
| `SENTRY_ENVIRONMENT` | Nom de l'environnement rapporte a Sentry (`development`, `production`, ...) |

## Migration de la base de donnees

Les tables (`utilisateurs`, `clients`, `contrats`, `evenements`) sont gerees
par Alembic. Une fois `DATABASE_URL` configure dans `.env` :

```bash
alembic upgrade head
```

## Creation du premier administrateur

Le CRUD des collaborateurs (`python main.py user create`) necessite deja
d'etre connecte avec un compte de role `gestion` : il faut donc un premier
compte pour amorcer une base vide. Le script `scripts/create_first_admin.py`
sert uniquement a ca et refuse de s'executer si un collaborateur existe deja
en base :

```bash
python scripts/create_first_admin.py
```

Il demande un email, un mot de passe, un prenom et un nom, puis cree un
collaborateur de role `gestion`. Toute creation ulterieure de collaborateur
doit ensuite passer par `python main.py user create` (une fois connecte).

## Utilisation

```bash
python main.py --help
```

### Connexion (`auth`)

| Commande | Description |
|---|---|
| `python main.py auth login` | Se connecter (email + mot de passe), ouvre une session locale valable 8h |
| `python main.py auth whoami` | Afficher le collaborateur actuellement connecte |
| `python main.py auth logout` | Fermer la session locale |

### Clients (`client`)

| Commande | Description | Role requis |
|---|---|---|
| `client create` | Creer un client (auto-associe au commercial connecte) | commercial |
| `client list` | Lister tous les clients | tous (lecture seule) |
| `client update <email>` | Modifier un client | commercial responsable du client |

### Contrats (`contract`)

| Commande | Description | Role requis |
|---|---|---|
| `contract create` | Creer un contrat pour un client existant | gestion |
| `contract list [--unsigned] [--unpaid]` | Lister les contrats, filtres optionnels | tous (lecture seule) |
| `contract update <contract_id>` | Modifier un contrat (montants, signature) | gestion, ou commercial responsable du client |

### Evenements (`event`)

| Commande | Description | Role requis |
|---|---|---|
| `event create` | Creer un evenement pour un contrat signe de son propre client | commercial |
| `event list [--no-support] [--mine]` | Lister les evenements, filtres optionnels | tous (lecture seule) |
| `event update <event_id>` | Modifier un evenement | support responsable de l'evenement |
| `event assign-support <event_id>` | Associer un collaborateur support a un evenement | gestion |

### Collaborateurs (`user`)

| Commande | Description | Role requis |
|---|---|---|
| `user create` | Creer un collaborateur | gestion |
| `user list` | Lister tous les collaborateurs | tous (lecture seule) |
| `user update <email>` | Modifier un collaborateur | gestion |
| `user delete <email>` | Supprimer un collaborateur | gestion |

Les commandes `update` proposent un menu interactif (choix du champ a
modifier), avec possibilite d'enchainer plusieurs modifications avant de
valider.

## Tests

```bash
pytest
```
