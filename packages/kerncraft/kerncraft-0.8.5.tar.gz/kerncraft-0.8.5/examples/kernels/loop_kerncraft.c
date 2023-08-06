double dx;
double dy;
double dz;
double ir;
double pos_x[N];
double pos_y[N];
double pos_z[N];
double force_cur_x[N];
double force_cur_y[N];
double force_cur_z[N];
double charges[N];

for(int i=0; i<N-1; i++)
{
    for(int j=0; j<N-1; j++)
    {
      dx = pos_x[i] - pos_x[j] ;
      dy = pos_y[i] - pos_y[j] ;
      dz = pos_z[i] - pos_z[j] ;

      ir = 1.0 / (dx*dx) + ((dy*dy) + (dz*dz));

      force_cur_x[i] = force_cur_x[i] + (charges[j] * dx * ir * ir * ir);
      force_cur_y[i] = force_cur_y[i] + (charges[j] * dy * ir * ir * ir);
      force_cur_z[i] = force_cur_z[i] + (charges[j] * dz * ir * ir * ir);
    }
}
