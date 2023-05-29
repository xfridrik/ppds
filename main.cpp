#include <stdio.h>
#include <mpi.h>
#include <limits.h>
#include <math.h>

#define INPUT "graphs/vstupy/graph_1000.txt"

void write_matrix(int p, int **matrix, int n) {
    char filename[50];
    sprintf(filename, "out_%dp.txt", p);

    FILE *fp = fopen(filename, "w");
    if (fp == nullptr) {
        printf("nepodarilo sa otvorit subor na zapis: %s\n", filename);
        return;
    }
    printf("Writing output to %s...\n", filename);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if(i==j || matrix[i][j]==INT_MAX) continue;
            fprintf(fp, "%d %d %d\n", i, j, matrix[i][j]);
        }
    }
    fclose(fp);
}


void send_rows(int p, int rank, int pc, int blockSize, int k, int **D, int n){
    int i, pci, count;
    count = (pc + blockSize > n) ? (n - pc) : blockSize;
    MPI_Request r;
    for (i = 0; (i < p); i++) { // send to all processes
        pci = (i % (int)sqrt(p)) * blockSize;
        if (i != rank && pci == pc && count > 0) {
            MPI_Isend(&D[k][pc], count, MPI_INT, i, 0, MPI_COMM_WORLD, &r);
        }
    }
}

void send_cols(int p, int rank, int pr, int blockSize, int k, int **D, int n){
    int i, j, pri, count;
    count = (pr + blockSize > n) ? (n - pr) : blockSize;
    int *colBuf = (int *) malloc(sizeof(int) * count);
    for (i = pr, j = 0; (j < count); i++, j++) {
        colBuf[j] = D[i][k]; //copy col k to buf
    }
    for (i = 0; (i < p); i++) {
        pri = (i / (int) sqrt(p)) * blockSize;
        if (i != rank && pri == pr && count > 0) {
            MPI_Request r;
            MPI_Isend(colBuf, count, MPI_INT, i, 1, MPI_COMM_WORLD, &r);
        }
    }
}

void receive_rows(int p, int rank, int pc, int blockSize, int k, int **D, int n){
    int i, pri, pci, count;
    for (i = 0; (i < p); i++) {
        pri = (i / (int) sqrt(p)) * blockSize;
        pci = (i % (int)sqrt(p)) * blockSize;
        count = (pci + blockSize > n) ? (n - pci) : blockSize;
        // receive from processes in same column which contain k-row segment
        if (i != rank && pc == pci && k >= pri && k < pri+blockSize && count > 0) {
            MPI_Recv(&D[k][pci], count, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
    }
}

void receive_cols(int p, int rank, int pr, int blockSize, int k, int **D, int n){
    int i, j, pri, pci, count;
    for (i = 0; (i < p); i++) {
        pri = (i / (int) sqrt(p)) * blockSize;
        pci = (i % (int)sqrt(p)) * blockSize;
        count = (pri + blockSize > n) ? (n - pri) : blockSize;
        // receive from processes in same row which contain k-column segment
        if (i != rank && pri == pr && k >= pci && k < pci+blockSize && count > 0) {
            int *colBuf = (int *) malloc(sizeof(int) * count);
            MPI_Recv(colBuf, count, MPI_INT, i, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            for (j = 0; j < count; j++){
                D[pri+j][k] = colBuf[j]; // copy back to D
            }
        }
    }
}

void merge_matrix(int p, int rank, int pr, int pc, int blockSize, int k, int **D, int n){
    int i, j, pri, pci, count;
    if (rank == 0) {
        /** receive all row segments by 0 **/
        for (i = 1; i < p; i++) {
            pri = (i / (int) sqrt(p)) * blockSize;
            pci = (i % (int)sqrt(p)) * blockSize;
            for(j=0; (j < blockSize && pri+j < n); j++){
                count = (pci + blockSize > n) ? (n - pci) : blockSize;
                if(count > 0){
                    MPI_Recv(&D[pri+j][pci], count, MPI_INT, i, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                }
            }
        }
    } else {
        /** send all row segments to 0 **/
        for(j=0; (j < blockSize && pr+j < n); j++){
            count = ((pc + blockSize) > n) ? (n - pc) : blockSize;
            if(count > 0){
                int *Buf = (int *) malloc(sizeof(int) * count);
                for (k = 0; (k < count); k++) {
                    Buf[k] = D[pr+j][pc+k];
                }
                MPI_Request r;
                MPI_Isend(Buf, count, MPI_INT, 0, 2, MPI_COMM_WORLD, &r);
            }
        }
    }
}

/** Parallel floydWarshall using 2D block mapping
 * Arguments:
 * D - input 2D matrix
 * rank - process rank
 * p - count of processes (square)
 * n - length of matrix **/

void my_floydWarshall_2d_2(int **D, int rank, int p, int n){
    int blockSize, i, j, k;
    if(rank>=p){
        blockSize = 0;
    }else{
        blockSize = ceil(n / sqrt(p));
    }
    int pr = (rank / (int)sqrt(p)) * blockSize; // begin row
    int pc = (rank % (int)sqrt(p)) * blockSize; // begin column
    //printf("proc %i: D[%i][%i] size %i\n", rank, pr, pc, blockSize);

    for (k = 0; k < n; k++) {

        /** each process with segment of the kth row of D send it to the P[*,pc] processes **/
        if(k >= pr && k < pr+blockSize) { //contains kth row
            send_rows(p, rank, pc, blockSize, k, D, n);
        }

        /** each process with segment of the kth column of D send it to the P[pr,*] processes **/
        if(k >= pc && k < pc+blockSize) { //contains kth col
            send_cols(p, rank, pr, blockSize, k, D, n);
        }

        /** receive row segments **/
        receive_rows(p, rank, pc, blockSize, k, D, n);

        /** receive col segments **/
        receive_cols(p, rank, pr, blockSize, k, D, n);

        /** calculate distances **/
        for (i = pr; (i < n && i < pr+blockSize); i++) { //row i
            for (j = pc; (j < n && j < pc+blockSize); j++) { //col j
                if (i == j) continue;
                if (D[i][k] != INT_MAX && D[k][j] != INT_MAX && D[i][j] > D[i][k] + D[k][j]) {
                    D[i][j] = D[i][k] + D[k][j];
                }
            }
        }
        MPI_Barrier(MPI_COMM_WORLD);
    }

    /** send all segments to 0 **/
    merge_matrix(p, rank, pr, pc, blockSize, k, D, n);
}



void print_matrix(int **D, int n){
    int i,j;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            if (D[i][j] == INT_MAX) {
                printf("%5s", "X");
            } else {
                printf("%5d", D[i][j]);
            }
        }
        printf("\n");
    }
}

int **load(char *filename, int *n_out){
    int n, x, y, value;
    FILE *fp;

    fp = fopen(filename, "r"); // open input file
    if (fp == nullptr) {
        printf("nepodarilo sa otvorit subor na citanie: %s\n", filename);
        exit(1);
    }

    fscanf(fp, "%d", n_out); // first line - size
    n = *n_out;

    int **matrix = (int **)malloc(n * sizeof(int *)); //allocate for line pointers
    for (int i = 0; i < n; i++) {
        matrix[i] = (int *)malloc(n * sizeof(int)); //allocate line
        for (int j = 0; j < n; j++) {
            if(i==j){
                matrix[i][j] = 0; // init diagonal to 0
            }else{
                matrix[i][j] = INT_MAX; // others init to max
            }
        }
    }
    while (fscanf(fp, "%d %d %d", &x, &y, &value) == 3) {
        matrix[x][y] = value;
    }
    fclose(fp);
    return matrix;
}

int main(int argc, char *argv[]) {
    int **matrix;
    int n, i, size, rank;

    // load matrix from file
    matrix = load(INPUT, &n);

    // init MPI
    MPI_Init(nullptr, nullptr);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // size must be square
    for (i = sqrt(size); i >= 0; i--) {
        if (i*i <= size) {
            size = i*i;
            break;
        }
    }

    // count time for rank 0
    if(rank == 0){
        printf("Pocitam so stvorcovym poctom procesorov: %d\n", i*i);

        double start_t = MPI_Wtime();;

        my_floydWarshall_2d_2(matrix, rank, size, n);

        double end_t = MPI_Wtime();
        double total = ((double) (end_t - start_t)) * 1000.0;
        printf("Total compute time: %lf milliseconds\n", total);
        write_matrix(size, matrix, n);
        //print_matrix(matrix,n);

    }else{
        my_floydWarshall_2d_2(matrix, rank, size, n);
    }

    for (i = 0; i < n; i++) {
        free(matrix[i]);
    }
    free(matrix);

    MPI_Finalize();

    return 0;
}
