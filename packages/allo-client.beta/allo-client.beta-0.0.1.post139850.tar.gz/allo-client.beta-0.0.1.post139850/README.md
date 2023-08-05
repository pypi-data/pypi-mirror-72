# Allo client

Paquet Python3 permettant la télémaintenance et la mise à jour automatique des logiciel Libriciel-SCOP.
- Demande identifiant client
- Demande code produit
- Association avec code PIN via le serveur Allo
- Demande de token de télémaintenance
- Clone du repo gitlab

Une fois activé, il est possible de :
- Lancer la télémaintenance via le système "Teleport"
- mettre à jour automatiquement
- annuler une mise à jour automatiquement

## Communications réseau

Allo-client doit pouvoir communiquer avec :
- `allo.dev.libriciel.fr:443`

## Installation

Toutes les commandes suivantes sont à lancer en tant qu'utilisateur `root`.

### Pré-requis RHEL / CentOS

v7 :
```bash
yum install epel-release
yum install python-pip
```

Général :
```bash
yum install python36
```

### Pré-requis Debian / Ubuntu

```bash
apt update && apt install python3-pip python-pip
```

### Installation

```bash
pip install ansible
pip3 install allo-client
allo-install
```

## Reste à faire

- Installation automatique de "ansible"
- Création automatique d'utilisateur spécifique lors de la validation du client (sous la forme libriciel-**produit**)
- Mise à jour des informations de connexion



