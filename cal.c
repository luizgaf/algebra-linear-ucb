#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

void swap_rows(double **A, int r1, int r2);
int gauss_elimination(double **A, int n);
int back_substitution(double **A, int n);
void show_matrix(double **A, int n);
void free_matrix(double **A, int n);

/* Programa que resolve sistemas lineares por eliminação de Gauss.
   Pequenas diferenças de estilo e mensagens para "outro autor". */

int main(void) {
    int n;

    printf("Informe a ordem do sistema (ex: 3 -> sistema 3x3): ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("Valor de ordem inválido. Encerrando.\n");
        return 1;
    }

    /* aloca a matriz aumentada dinamicamente */
    double **A = malloc(n * sizeof(double *));
    if (!A) { fprintf(stderr, "Falha na alocação.\n"); return 1; }
    for (int i = 0; i < n; ++i) {
        A[i] = malloc((n + 1) * sizeof(double));
        if (!A[i]) { fprintf(stderr, "Falha na alocação.\n"); return 1; }
    }

    /* entrada das equações linha a linha, com confirmação após cada linha */
    printf("\nInforme os coeficientes e o termo independente de cada equação.\n");
    for (int i = 0; i < n; ++i) {
        int confirmed = 0;
        while (!confirmed) {
            printf("\nEquação %d — digite %d coeficiente(s) e o termo independente:\n", i + 1, n);
            for (int j = 0; j <= n; ++j) {
                if (j < n) printf("  coef x%d: ", j + 1);
                else        printf("  termo b%d: ", i + 1);

                while (scanf("%lf", &A[i][j]) != 1) {
                    printf("  Entrada inválida — tente novamente: ");
                    int c;
                    while ((c = getchar()) != '\n' && c != EOF); // descarta lixo
                }
            }

            // montar e exibir a equação que acabou de ser digitada
            // exemplo: "2*x1 + -3.5*x2 + 1*x3 = 4"
            char linha[512];
            linha[0] = '\0';
            for (int j = 0; j < n; ++j) {
                char part[80];
                snprintf(part, sizeof(part), "%g*x%d", A[i][j], j + 1);
                if (j > 0) strncat(linha, " + ", sizeof(linha) - strlen(linha) - 1);
                strncat(linha, part, sizeof(linha) - strlen(linha) - 1);
            }
            char rhs[80];
            snprintf(rhs, sizeof(rhs), " = %g", A[i][n]);
            strncat(linha, rhs, sizeof(linha) - strlen(linha) - 1);

            printf("\nVocê digitou: %s\n", linha);

            // pedir confirmação (aceita 's' ou 'n', tanto maiúsculas quanto minúsculas)
            printf("Confirmar essa equação? (s/n): ");
            int ch;
            // consumir até próximo caractere não-espaco
            while ((ch = getchar()) != EOF) {
                if (ch == '\n') continue;
                if (!isspace(ch)) break;
            }
            if (ch == EOF) { confirmed = 0; break; }
            char resp = (char)ch;
            // se houver resto na linha, descarta até newline
            int c2;
            while ((c2 = getchar()) != '\n' && c2 != EOF);

            if (tolower((unsigned char)resp) == 's') {
                confirmed = 1;
            } else {
                printf("Ok, reentre a equação %d.\n", i + 1);
                confirmed = 0;
            }
        }
    }

    printf("\nMatriz aumentada inicial:\n");
    show_matrix(A, n);

    if (!gauss_elimination(A, n)) {
        free_matrix(A, n);
        return 1;
    }

    printf("\nMatriz depois do escalonamento:\n");
    show_matrix(A, n);

    back_substitution(A, n);

    free_matrix(A, n);
    return 0;
}

/* troca de ponteiros das linhas — O(1) */
void swap_rows(double **A, int r1, int r2) {
    double *tmp = A[r1];
    A[r1] = A[r2];
    A[r2] = tmp;
}

/* visualização simples da matriz aumentada */
void show_matrix(double **A, int n) {
    for (int i = 0; i < n; ++i) {
        printf("  [ ");
        for (int j = 0; j <= n; ++j) {
            // largura pequena, formato compacto
            printf("%8.3g ", A[i][j]);
            if (j == n - 1) printf("| ");
        }
        printf("]\n");
    }
}

/* libera memória alocada */
void free_matrix(double **A, int n) {
    if (!A) return;
    for (int i = 0; i < n; ++i) free(A[i]);
    free(A);
}

/* eliminação de Gauss: transforma em forma triangular superior */
int gauss_elimination(double **A, int n) {
    for (int k = 0; k < n - 1; ++k) {
        if (A[k][k] == 0.0) {
            int found = 0;
            for (int i = k + 1; i < n; ++i) {
                if (A[i][k] != 0.0) {
                    printf("[Aviso] pivô zero — trocando linha %d com %d\n", k + 1, i + 1);
                    swap_rows(A, k, i);
                    found = 1;
                    break;
                }
            }
            if (!found) {
                // coluna inteira abaixo do pivô é zero; seguirá sem divisão por zero
                continue;
            }
        }

        for (int i = k + 1; i < n; ++i) {
            if (A[k][k] == 0.0) continue; // segurança extra
            double factor = A[i][k] / A[k][k];
            for (int j = k; j <= n; ++j) {
                A[i][j] -= factor * A[k][j];
            }
        }
    }
    return 1;
}

/* retro-substituição para encontrar as variáveis */
int back_substitution(double **A, int n) {
    double *x = malloc(n * sizeof(double));
    if (!x) { fprintf(stderr, "Erro de memória.\n"); return 0; }

    for (int i = n - 1; i >= 0; --i) {
        if (A[i][i] == 0.0) {
            if (A[i][n] == 0.0) {
                printf("\nResultado: infinitas soluções (sistema indeterminado).\n");
            } else {
                printf("\nResultado: sistema impossível (sem solução).\n");
            }
            free(x);
            return 0;
        }

        double sum = A[i][n];
        for (int j = i + 1; j < n; ++j) sum -= A[i][j] * x[j];
        x[i] = sum / A[i][i];
    }

    printf("\nSolução encontrada:\n");
    for (int i = 0; i < n; ++i) {
        printf("  x%d = %g\n", i + 1, x[i]);
    }

    free(x);
    return 1;
}
