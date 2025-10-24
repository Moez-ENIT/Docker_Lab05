# Architecture de l'application


L’architecture met en place une application multi-services orchestrée par **Docker Compose**, structurée autour d’un réseau Docker interne qui relie plusieurs conteneurs interdépendants.

### Couche de supervision et de monitoring

En haut de la pile, **Grafana** fournit une interface de visualisation des métriques sous forme de tableaux de bord. Il se connecte à **Prometheus**, qui collecte (scrape) les métriques exposées par les différents services du système, notamment l’application Flask.

### Couche réseau et application

Tous les services communiquent à l’intérieur d’un **réseau Docker** isolé, garantissant la connectivité et la sécurité interne.
Au centre de ce réseau se trouve **Traefik**, un reverse proxy et load balancer moderne.

* Traefik reçoit les requêtes entrantes sur les ports **:80**, **:8080** (interface de Traefik), et **:443** (HTTPS).
* Il distribue ces requêtes vers les **applications Flask** selon les règles de routage définies par les labels Docker.

Les **applications Flask** constituent la couche logique du système.
Elles traitent les requêtes API, accèdent aux bases de données et publient des métriques pour Prometheus.

### Couche frontend et données

* Le **serveur Nginx** héberge la partie **frontend** statique (HTML, CSS, JavaScript) et redirige les appels API vers les services Flask via Traefik.
* **PostgreSQL** gère la **base de données relationnelle**, tandis que **Redis** sert de **cache** et de **stockage rapide en mémoire** pour certaines opérations de performance ou de comptage.


## Flux de données global
**Utilisateur → Traefik → Nginx (frontend) → Flask (backend) → PostgreSQL / Redis**,
tandis que les métriques sont collectées par **Prometheus** et visualisées dans **Grafana**.


## Travail demandé
> [!IMPORTANT]
> Completer les fichiers **docker-compose.yml** pour que l'application fonctionne correctement.
> Les donnees sensibles (login et password) ne doivent pas apparaitre enn clair dans le fichier docker-compose.yml.
> Si les fichiers fournis contiennent des erreurs il faut les corriger.
> Faire le **push** du projet.
