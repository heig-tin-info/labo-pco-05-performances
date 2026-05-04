# Labo Performance <!-- omit in toc -->

L'objectif de ce travail pratique est de mettre en évidence certains mécanismes internes au processeur qui limitent les performances d'exécution d'un programme. Ce travail est principalement basé sur l'excellent référentiel de [Kobzol](https://github.com/Kobzol/hardware-effects).

| Type       | Description                        |
| ---------- | ---------------------------------- |
| Durée      | 2x45 minutes + Travail à la maison |
| Rendu      | Sur GitHub                         |
| Format     | Travail individuel                 |
| Évaluation | Sur la base des livrables fournis  |

## Table des matières <!-- omit in toc -->

- [Prérequis](#prérequis)
- [Consignes](#consignes)
- [Informations du cache](#informations-du-cache)
- [Installation de Perf](#installation-de-perf)
- [Expérience n°1 : Prédiction d'embranchements](#expérience-n1--prédiction-dembranchements)
- [Expérience n°2 : Latences de la SDRAM](#expérience-n2--latences-de-la-sdram)
- [Expérience n°3 : False Sharing](#expérience-n3--false-sharing)
- [Expérience n°4 : Cache locality](#expérience-n4--cache-locality)
- [Conclusion](#conclusion)

## Prérequis

- Lire le chapitre [Mémoire cache](https://heig-tin-info.github.io/handbook/course-concurrent/memory/) du cours de programmation concurrente.

## Consignes

- Parcourir la donnée du travail pratique et exécutez les différents programmes.
- Rédiger un rapport (possiblement avec Jupyter Notebook) pour mettre en évidence vos résultats.
- Rédigez une conclusion personnelle sur ce travail pratique en expliquant ce que vous avez appris
- Faites un commit et push de votre travail sur GitHub, incluant le rapport.

**Vous pouvez inclure votre rapport à vos notes personnelles pour le livrable de fin de semestre.**

## Informations du cache

Sous linux, vous devriez pouvoir obtenir les informations sur le cache mémoire avec la commande:

```bash
getconf -a | grep CACHE
```

1. Combien de niveaux de cache avez-vous sur votre ordinateur ?
2. Quelle est la taille d'une **ligne de cache** en bytes ?
3. Quels sont les tailles des caches pour chaque niveau en KiB ?

## Installation de Perf

Vous aurez besoin de l'outil `perf`. Sur Ubuntu/Debian/WSL :

```bash
sudo apt install linux-tools-common linux-tools-generic linux-tools-$(uname -r)
```

Si la dernière commande échoue (notamment sous WSL où le paquet pour le noyau courant n'est pas toujours disponible), repliez-vous sur `linux-tools-generic` seul, ou suivez la procédure de compilation depuis les sources du noyau.

> **Note WSL2 / VM** : la virtualisation peut perturber les compteurs `perf` et les mesures de l'expérience n°2 (DRAM refresh). Les ordres de grandeur restent observables, mais attendez-vous à plus de bruit qu'en bare metal.

> **Note Linux** : si vous utilisez une autre distribution qu'Ubuntu/Debian, la procédure d'installation de `perf` peut différer. Consultez la documentation de votre distribution pour plus d'informations.

## Expérience n°1 : Prédiction d'embranchements

Prendre connaissance du programme [branch-misprediction.cpp](branch-misprediction.cpp). Compiler et exécutez le avec la commande:

```bash
g++ -O3 -o branch-misprediction branch-misprediction.cpp
perf stat -e branches,branch-misses ./branch-misprediction 0
perf stat -e branches,branch-misses ./branch-misprediction 1
```

1. Quelle est la différence entre les deux exécutions ?
2. Pouvez-vous expliquer pourquoi ?
3. Reportez le ratio `branch-misses / branches` pour les deux exécutions.
4. Que pensez-vous de la question StackOverflow [Why is it faster to process a sorted array than an unsorted array?](https://stackoverflow.com/questions/11227809/why-is-it-faster-to-process-a-sorted-array-than-an-unsorted-array) et du nombre de upvotes ?

## Expérience n°2 : Latences de la SDRAM

Prendre connaissance du programme [dram-refresh.cpp](dram-refresh.cpp).

Compiler et exécutez le avec la commande:

```bash
g++ -O3 -o dram-refresh dram-refresh.cpp
./dram-refresh > dram-refresh.dat
python3 dram-refresh.py dram-refresh.dat
```

1. Que constatez-vous ?
2. Comment expliquez-vous ces résultats ?
3. Trouvez-vous une correspondance de vos résultats [ici](https://en.wikipedia.org/wiki/Memory_refresh) ?

## Expérience n°3 : False Sharing

Compilez et exécutez le programme [false-sharing.cpp](false-sharing.cpp) avec la commande:

```bash
g++ -O3 -o false-sharing false-sharing.cpp
perf stat -d ./false-sharing 3 1
perf stat -d ./false-sharing 3 8
...
```

Le premier argument est le **nombre de threads**, le second est le **pas (`increment`)** entre les éléments incrémentés par chaque thread. Comme `sizeof(size_t)` vaut 8 octets et qu'une ligne de cache fait 64 octets, un `increment` de 1 place tous les threads sur la **même ligne de cache** (situation pathologique de *false sharing*), tandis qu'un `increment` de 8 garantit qu'ils sont sur des lignes **distinctes**.

1. Que constatez-vous ?
2. Comment expliquez-vous ces résultats ?
3. Quel est le comportement en faisant varier les différents paramètres (nombre de threads, valeurs intermédiaires d'`increment` entre 1 et 8) ?

## Expérience n°4 : Cache locality

Prendre connaissance du programme [locality.cpp](locality.cpp). Compilez avec et sans la macro `LINE` :

```bash
g++ -O3 -DLINE -o locality-line locality.cpp
g++ -O3       -o locality-col  locality.cpp
perf stat -e cache-references,cache-misses ./locality-line
perf stat -e cache-references,cache-misses ./locality-col
```

Faites varier `N` (par exemple 1000, 2000, 5000, 10000) pour observer l'évolution du rapport entre les deux versions.

1. Que fait le programme
2. Quelle est la différence entre les deux exécutions ?
3. Comment expliquez-vous ces résultats ?

## Conclusion

Rédigez une conclusion personnelle sur ce travail pratique en expliquant ce que vous avez appris.

Expliquez pourquoi les concepts de cache, de prédiction d'embranchements, de latences de la SDRAM, de false sharing et de cache locality sont importants pour un développeur de logiciel, spécialement pour ceux qui souhaitent paralleliser leur code pour obtenir de meilleures performances.

Faites un parallèle avec la programmation concurrente : comment les mécanismes internes du processeur peuvent-ils impacter les performances d'un programme concurrent tournant sur plusieurs threads ou processus ? Quels sont les pièges à éviter et les bonnes pratiques à adopter pour tirer le meilleur parti du matériel tout en évitant les problèmes de performance liés à ces mécanismes ?
