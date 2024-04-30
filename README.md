# Labo Performance <!-- omit in toc -->

L'objectif de ce travail pratique et de mettre en évidence certains mécanismes internes au processeur qui limitent les performances d'exécution d'un programme. Ce travail est principalement basé sur l'excellent référentiel de [Kobzol](https://github.com/Kobzol/hardware-effects).

| Type          | Description |
| ------------- | ----------- |
| Durée         | 3x45 minutes + Travail à la maison |
| Rendu         | Sur GitHub |
| Format | Travail individuel |
| Évaluation | Sur la base des livrables fournis |

## Table des matières <!-- omit in toc -->

- [Objectifs](#objectifs)
- [Informations du cache](#informations-du-cache)
- [Installation de Perf](#installation-de-perf)
- [Expérience n°1 : Prédiction d'embranchements](#expérience-n1--prédiction-dembranchements)
- [Expérience n°2 : Latences de la SDRAM](#expérience-n2--latences-de-la-sdram)
- [Expérience n°3 : False Sharing](#expérience-n3--false-sharing)
- [Expérience n°4 : Cache locality](#expérience-n4--cache-locality)
- [Conclusion](#conclusion)

## Objectifs

- Parcourir la donnée du travail pratique et exécutez les différents programmes.
- Rédiger un rapport (possiblement avec Jupyter Notebook) pour mettre en évidence vos résultats.
- Rédigez une conclusion personnelle sur ce travail pratique en expliquant ce que vous avez appris
- Faites un commit et push de votre travail sur GitHub, incluant le rapport.

## Informations du cache

Sous linux, vous devriez pouvoir obtenir les informations sur le cache mémoire avec la commande:

```
getconf -a | grep CACHE
```

1. Combien de niveaux de cache avez-vous sur votre ordinateur ?
2. Quelle es la taille d'une ligne de cache en bytes ?
3. Quels sont les tailles des caches pour chaque niveau en KiB ?

## Installation de Perf

Vous aurez besoin de l'outil `perf`. On vous propose la démarche suivante :

```bash
git clone --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
cd linux/tools/perf
sudo apt install flex bison libdw-dev elfutils systemtap-sdt-dev libelf-dev libunwind-dev libcapstone-dev libpfm4-dev libcrypto++-dev perl libperl-dev libcap-dev libzstd-dev libbabeltrace-dev libslang2-dev libtraceevent-dev libssl-dev asciidoc
make
cp perf /usr/bin
```

## Expérience n°1 : Prédiction d'embranchements

Prendre connaissance du programme [branch-misprediction.cpp](branch-misprediction.cpp). Compiler et exécutez le avec la commande:

```bash
g++ -O3 -o branch-misprediction branch-misprediction.cpp
perf -e branches,branch-misses ./branch-misprediction 0
perf -e branches,branch-misses ./branch-misprediction 1
```

1. Quelle est la différence entre les deux exécutions ?
2. Pouvez-vous expliquer pourquoi ?
3. Que pensez-vous de la question StackOverflow [Why is it faster to process a sorted array than an unsorted array?](https://stackoverflow.com/questions/11227809/why-is-it-faster-to-process-a-sorted-array-than-an-unsorted-array) et du nombre de upvotes ?

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

1. Que constatez-vous ?
2. Comment expliquez-vous ces résultats ?
3. Quel est le comportement en faisant varier les différents paramètres ?

## Expérience n°4 : Cache locality

Prendre connaissance du programme [locality.cpp](locality.cpp). Compiler et exécutez le code avec l'option `LINE` activée et désactivée. Ajustez la taille du tableau pour obtenir des temps de calculs significatifs.

Utilisez `perf` pour votre analyse.

1. Que fait le programme
2. Quelle est la différence entre les deux exécutions ?
3. Comment expliquez-vous ces résultats ?

## Conclusion

Rédigez une conclusion personnelle sur ce travail pratique en expliquant ce que vous avez appris.

Expliquez pourquoi les concepts de cache, de prédiction d'embranchements, de latences de la SDRAM, de false sharing et de cache locality sont importants pour un développeur de logiciel, spécialement pour ceux qui souhaitent paralleliser leur code pour obtenir de meilleures performances.
