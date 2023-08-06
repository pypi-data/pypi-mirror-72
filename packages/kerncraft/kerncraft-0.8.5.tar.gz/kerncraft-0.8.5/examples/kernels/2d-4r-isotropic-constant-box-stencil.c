double a[M][N];
double b[M][N];
double c0;
double c1;
double c2;
double c3;
double c4;
double c5;
double c6;
double c7;
double c8;

for(int j=4; j < M-4; j++){
for(int i=4; i < N-4; i++){
b[j][i] = c0 * a[j][i]
+ c1 * (a[j][i-1] + a[j-1][i] + a[j+1][i] + a[j][i+1])
+ c2 * (a[j][i-2] + a[j-1][i-1] + a[j+1][i-1] + a[j-2][i] + a[j+2][i] + a[j-1][i+1] + a[j+1][i+1] + a[j][i+2])
+ c3 * (a[j][i-3] + a[j-1][i-2] + a[j+1][i-2] + a[j-2][i-1] + a[j+2][i-1] + a[j-3][i] + a[j+3][i] + a[j-2][i+1] + a[j+2][i+1] + a[j-1][i+2] + a[j+1][i+2] + a[j][i+3])
+ c4 * (a[j][i-4] + a[j-1][i-3] + a[j+1][i-3] + a[j-2][i-2] + a[j+2][i-2] + a[j-3][i-1] + a[j+3][i-1] + a[j-4][i] + a[j+4][i] + a[j-3][i+1] + a[j+3][i+1] + a[j-2][i+2] + a[j+2][i+2] + a[j-1][i+3] + a[j+1][i+3] + a[j][i+4])
+ c5 * (a[j-1][i-4] + a[j+1][i-4] + a[j-2][i-3] + a[j+2][i-3] + a[j-3][i-2] + a[j+3][i-2] + a[j-4][i-1] + a[j+4][i-1] + a[j-4][i+1] + a[j+4][i+1] + a[j-3][i+2] + a[j+3][i+2] + a[j-2][i+3] + a[j+2][i+3] + a[j-1][i+4] + a[j+1][i+4])
+ c6 * (a[j-2][i-4] + a[j+2][i-4] + a[j-3][i-3] + a[j+3][i-3] + a[j-4][i-2] + a[j+4][i-2] + a[j-4][i+2] + a[j+4][i+2] + a[j-3][i+3] + a[j+3][i+3] + a[j-2][i+4] + a[j+2][i+4])
+ c7 * (a[j-3][i-4] + a[j+3][i-4] + a[j-4][i-3] + a[j+4][i-3] + a[j-4][i+3] + a[j+4][i+3] + a[j-3][i+4] + a[j+3][i+4])
+ c8 * (a[j-4][i-4] + a[j+4][i-4] + a[j-4][i+4] + a[j+4][i+4])
;
}
}
