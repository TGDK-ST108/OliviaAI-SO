#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define SECTOR_COUNT 5
#define MAX_DATA_LEN 256

// Currogation matrix container
double currogation_matrix[SECTOR_COUNT][SECTOR_COUNT];

// Generate sine-based vector sequences
void initialize_vector_sequences(double vectors[SECTOR_COUNT][SECTOR_COUNT]) {
    for (int i = 0; i < SECTOR_COUNT; i++) {
        for (int j = 0; j < SECTOR_COUNT; j++) {
            vectors[i][j] = sin(2 * M_PI * j / SECTOR_COUNT);
        }
    }
}

// Generate currogation matrix
void generate_currogation_matrix(double vectors[SECTOR_COUNT][SECTOR_COUNT]) {
    for (int i = 0; i < SECTOR_COUNT; i++) {
        for (int j = 0; j < SECTOR_COUNT; j++) {
            currogation_matrix[i][j] = vectors[i][j] * (i + 1);
        }
    }
}

// Apply propagated currogation
void apply_currogation(char *input, double *output) {
    size_t len = strlen(input);
    for (size_t i = 0; i < len; i++) {
        double mod = (double)input[i];
        for (int j = 0; j < SECTOR_COUNT; j++) {
            mod += currogation_matrix[i % SECTOR_COUNT][j];
        }
        output[i] = mod;
    }
}

// Print symbolic chart from currogated data
void print_symbolic_chart(double *data, size_t len) {
    printf("Symbolic Glyph Chart:\n");
    for (size_t i = 0; i < len; i++) {
        int symbol_code = 0x2600 + ((int)data[i] % 96);
        printf("%lc ", (wint_t)symbol_code);  // Wide character output
    }
    printf("\n");
}

int main() {
    setlocale(LC_CTYPE, "");  // Enable Unicode output

    char *input_data[] = {"seed_flower", "pattern_144"};
    double vector_sequences[SECTOR_COUNT][SECTOR_COUNT];
    initialize_vector_sequences(vector_sequences);
    generate_currogation_matrix(vector_sequences);

    for (int i = 0; i < 2; i++) {
        char *input = input_data[i];
        double modulated[MAX_DATA_LEN] = {0};
        apply_currogation(input, modulated);
        print_symbolic_chart(modulated, strlen(input));
    }

    return 0;
}