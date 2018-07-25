

// NOT TESTED

int N = 100;
float P = .5;   // global probability
float p;        // local probability
int num0 = N*N*(1-p);
int num1 = N*N*p;
float random;

int** map = (int**)malloc(N*sizeof(int*));
int* temp;

for(int i = 0; i < N; i++)
{
  temp = new int[N];
  for(int j = 0; j < N; j++)
    temp[j] = -1;
  map[i] = temp;
}

for(int i = 0; i < N; i++)
{
  for(int j = 0; j < N; j++)
  {
    if(map[i][j] != -1)
    {
      p = (float)(num1/(num0 + num1));
      // random = random.normal(0,1);
      if(random < p)
      {
        map[i][j] = 1;
        num1--;
        // build a queue, don't do this recursively
        //floodFill(i, j , 1)
      }
      else
      {
        map[i][j] = 0;
        num0--;
        // build a queue, don't do this recursively
        //floodFill(i, j , 0)
      }
    }
  }
}
