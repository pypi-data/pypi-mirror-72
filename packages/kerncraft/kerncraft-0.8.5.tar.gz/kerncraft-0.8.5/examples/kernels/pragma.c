double a[1000*1000];

#pragma foo
#pragma bar
for(int i=0; i<1000; i++) {
    #pragma foo
    #pragma bar
    for(int j=0; j<1000; j++) {
        a[i*j] = 0.1;
    }
}
