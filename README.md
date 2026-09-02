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

### Schema de la base de donnees

```mermaid
erDiagram
    UTILISATEURS ||--o{ CLIENTS : "suit (commercial)"
    UTILISATEURS ||--o{ EVENEMENTS : "assure (support)"
    CLIENTS ||--o{ CONTRATS : possede
    CONTRATS ||--o{ EVENEMENTS : genere

    UTILISATEURS {
        uuid id PK
        string email
        string password_hash
        string first_name
        string last_name
        enum role
        datetime created_at
    }
    CLIENTS {
        uuid id PK
        string first_name
        string last_name
        string email
        string phone
        string company
        datetime created_at
        datetime last_contact_at
        uuid commercial_id FK
    }
    CONTRATS {
        uuid id PK
        decimal total_amount
        decimal remaining_amount
        datetime created_at
        boolean signed
        uuid client_id FK
    }
    EVENEMENTS {
        uuid id PK
        string event_name
        uuid contract_id FK
        datetime date_start
        datetime date_end
        string location
        int attendees
        text notes
        uuid support_id FK
    }
```

## Creation du premier administrateur

Le CRUD des collaborateurs (`python main.py user create`) necessite deja
d'etre connecte avec un compte de role `gestion` : il faut donc un premier
compte pour amorcer une base vide. Le script `scripts/create_first_admin.py`
sert uniquement a ca et refuse de s'executer si un collaborateur existe deja
en base :

```bash
python -m scripts/create_first_admin.py
```

Il demande un email, un mot de passe, un prenom et un nom, puis cree un
collaborateur de role `gestion`. Toute creation ulterieure de collaborateur
doit ensuite passer par `python main.py user create` (une fois connecte).

## Utilisation

```bash
python main.py --help
python main.py <groupe> --help        # ex: python main.py client --help
```

La CLI est organisee en 5 groupes de commandes : `auth`, `user`, `client`,
`contract`, `event`. Toutes les commandes (sauf `auth login`) necessitent
une session active (`python main.py auth login`), sans quoi elles echouent
avec `Vous devez etre connecte. Utilisez 'auth login'.` (code de sortie 1).

Les commandes `update` (client, contrat, evenement, collaborateur)
fonctionnent toutes de la meme facon : un menu interactif `Champ a
modifier` propose la liste des champs modifiables, demande la nouvelle
valeur puis affiche le resultat ; a la fin, `Modifier un autre champ ? [o/n]`
permet d'enchainer plusieurs modifications avant de quitter. Un acces
refuse affiche `Acces refuse.` et arrete la commande (code de sortie 1).

### Connexion (`auth`)

| Commande | Description | Role requis |
|---|---|---|
| `python main.py auth login` | Se connecter (demande `email` puis `mot de passe`), ouvre une session locale valable 8h | tous |
| `python main.py auth whoami` | Afficher le collaborateur actuellement connecte (nom, prenom, role) | tous (connecte) |
| `python main.py auth logout` | Fermer la session locale en cours | tous (connecte) |

En cas d'echec d'authentification (email/mot de passe incorrect),
`auth login` affiche `Authentification echouee.` et quitte avec le code 1.

### Collaborateurs (`user`)

| Commande | Description | Role requis |
|---|---|---|
| `python main.py user create` | Creer un collaborateur | gestion |
| `python main.py user list` | Lister tous les collaborateurs (prenom, nom, email, role) | tous (lecture seule) |
| `python main.py user show <email>` | Afficher le detail d'un collaborateur | tous (lecture seule) |
| `python main.py user update <email>` | Modifier un collaborateur existant | gestion |
| `python main.py user delete <email>` | Supprimer un collaborateur (confirmation demandee) | gestion |

**`user create`** demande successivement : `email`, `mot de passe`,
`prenom`, `nom`, puis `role` (choix parmi `gestion`, `commercial`,
`support`).

**`user update <email>`** — champs modifiables (`Champ a modifier`) :

| Champ | Valeur demandee |
|---|---|
| `email` | nouvel email |
| `mot-de-passe` | nouveau mot de passe (rehache) |
| `prenom` | nouveau prenom |
| `nom` | nouveau nom |
| `role` | nouveau role (`gestion`, `commercial`, `support`) |

**`user delete <email>`** demande une confirmation
(`Confirmer la suppression de <prenom> <nom> ?`) avant de supprimer
definitivement le collaborateur.

### Clients (`client`)

| Commande | Description | Role requis |
|---|---|---|
| `python main.py client create` | Creer un client, auto-associe au commercial connecte | commercial |
| `python main.py client list` | Lister tous les clients (prenom, nom, email, telephone, entreprise) | tous (lecture seule) |
| `python main.py client show <email>` | Afficher le detail d'un client | tous (lecture seule) |
| `python main.py client update <email>` | Modifier un client existant | commercial responsable du client |

**`client create`** demande : `prenom`, `nom`, `email`, `telephone`,
`nom de l'entreprise`. Le client cree est automatiquement rattache au
commercial actuellement connecte.

**`client update <email>`** — champs modifiables :

| Champ | Valeur demandee |
|---|---|
| `prenom` | nouveau prenom |
| `nom` | nouveau nom |
| `email` | nouvel email |
| `telephone` | nouveau telephone |
| `entreprise` | nouveau nom de l'entreprise |
| `dernier-contact` | date du dernier contact, format `JJ/MM/AAAA` |

### Evenements (`event`)

| Commande | Description | Role requis |
|---|---|---|
| `python main.py event create` | Creer un evenement pour un contrat signe de son propre client | commercial |
| `python main.py event list [--no-support] [--mine]` | Lister les evenements | tous (lecture seule) |
| `python main.py event show <event_id>` | Afficher le detail d'un evenement | tous (lecture seule) |
| `python main.py event update <event_id>` | Modifier un evenement existant | support responsable de l'evenement |
| `python main.py event assign-support <event_id>` | Associer un collaborateur support a un evenement | gestion |

**`event create`** demande : `nom de l'evenement`, `date de debut`
(`JJ/MM/AAAA HH:MM`), `date de fin` (`JJ/MM/AAAA HH:MM`), `lieu`,
`nombre de participants`, `notes`, puis `identifiant du contract` (uuid).
La creation echoue (`Contrat introuvable, non signe, ou non associe a
ce commercial.`) si le contrat n'existe pas, n'est pas signe, ou
n'appartient pas au commercial connecte.

**`event list`** :
- sans option : tous les evenements
- `--no-support` : uniquement les evenements sans support assigne
- `--mine` : uniquement les evenements dont le collaborateur connecte
  (support) est responsable

**`event update <event_id>`** — champs modifiables :

| Champ | Valeur demandee |
|---|---|
| `nom` | nouveau nom de l'evenement |
| `debut` | nouvelle date de debut, format `JJ/MM/AAAA HH:MM` |
| `fin` | nouvelle date de fin, format `JJ/MM/AAAA HH:MM` |
| `lieu` | nouveau lieu |
| `participants` | nouveau nombre de participants |
| `notes` | nouvelles notes |

**`event assign-support <event_id>`** demande `email du support a
assigner` ; renvoie `Collaborateur introuvable : <email>` si l'email ne
correspond a aucun collaborateur.

### Contrats (`contract`)

| Commande | Description | Role requis |
|---|---|---|
| `python main.py contract create` | Creer un contrat pour un client existant | gestion |
| `python main.py contract list [--unsigned] [--unpaid]` | Lister les contrats | tous (lecture seule) |
| `python main.py contract show <contract_id>` | Afficher le detail d'un contrat | tous (lecture seule) |
| `python main.py contract update <contract_id>` | Modifier un contrat (montants, signature) | gestion, ou commercial responsable du client |

**`contract create`** demande : `montant total a payer`,
`montant restant a payer` (format decimal, ex `1500.00`), puis
`email du client associe`. Renvoie `Client introuvable : <email>` si le
client n'existe pas.

**`contract list`** :
- sans option : tous les contrats
- `--unsigned` : uniquement les contrats non signes
- `--unpaid` : uniquement les contrats avec un reste a payer

**`contract update <contract_id>`** — champs modifiables :

| Champ | Valeur demandee |
|---|---|
| `montant-total` | nouveau montant total (decimal) |
| `montant-restant` | nouveau montant restant (decimal) |
| `signe` | contrat signe ? (`o`/`n`) |

La signature d'un contrat (`signe` -> `o`) est journalisee dans Sentry.

## Tests

```bash
pytest
```
