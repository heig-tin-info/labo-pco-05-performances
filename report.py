import matplotlib.pyplot as plt

# Lire les données depuis le fichier
steps = []
times = []

with open("results.csv", "r") as file:
    for line in file:
        parts = line.strip().split(", ")
        if len(parts) == 2:
            steps.append(int(parts[0]))
            times.append(float(parts[1]))

print(times)
# Création du graphique
plt.figure(figsize=(10, 5))
plt.plot(steps, times, marker='o')
#plt.xscale('log')  # Échelle logarithmique pour mieux voir les changements
plt.xlabel('Nombre d\'éléments accédés')
plt.ylabel('Temps (millisecondes)')
plt.title('Temps d\'accès en fonction du nombre d\'éléments')
plt.grid(True)
plt.show()
