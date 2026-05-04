#include <iostream>
#include <vector>
#include <chrono>

const int N = 10'000;

int main() {
    std::vector<int> matrix(static_cast<size_t>(N) * N, 0);

    for (size_t i = 0; i < N; i++)
        for (size_t j = 0; j < N; j++)
            matrix[i * N + j] = static_cast<int>(i * N + j);

    auto start = std::chrono::high_resolution_clock::now();
    long long sum = 0;
    for (size_t i = 0; i < N; i++)
        for (size_t j = 0; j < N; j++)
#ifdef LINE
            sum += matrix[i * N + j];
#else
            sum += matrix[j * N + i];
#endif
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> time = end - start;
#ifdef LINE
    std::cout << "Parcours par ligne (row-major) : " << sum << "\n";
#else
    std::cout << "Parcours par colonne (column-major) : " << sum << "\n";
#endif
    std::cout << "Temps d'acces: " << time.count() << " s" << std::endl;
}
