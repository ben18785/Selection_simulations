data{
  int N; // number of generations
  int K; // num variants
  int firstAppearance[K]; // generation when each variant first appears
  int mutantCounts[(N-1)]; // counts of mutant variants in each generation
  int counts[K,N]; // counts of variants in each generation
  int activeVariantCount[N]; // number of variants that have appeared thus far
}

parameters{
  real<lower=-1,upper=1> s;
  real<lower=0,upper=1> delta;
}

model{
  for(i in 1:(N-1)){
    vector[activeVariantCount[i]+1] f; // number of active variants + mutants
    int countsTemp[activeVariantCount[i]+1];
    for(j in 1:activeVariantCount[i]){
      f[j] = counts[j,i];
      countsTemp[j] = counts[j,(i+1)];
    }
    f[activeVariantCount[i]+1] = 0;
    countsTemp[activeVariantCount[i]+1] = mutantCounts[i];
    f = f / sum(f);
    f = f .* (1 + s * f);
    f[activeVariantCount[i]+1] = 0;
    f = f/sum(f);
    f = f * (1-delta);
    f[activeVariantCount[i]+1] = delta;
    countsTemp ~ multinomial(f);
  }
}

generated quantities{
  vector[N-1] vLogLikelihood;
  for(i in 1:(N-1)){
    vector[activeVariantCount[i]+1] f;
    int countsTemp[activeVariantCount[i]+1];
    for(j in 1:activeVariantCount[i]){
      f[j] = counts[j,i];
      countsTemp[j] = counts[j,(i+1)];
    }
    f[activeVariantCount[i]+1] = 0;
    countsTemp[activeVariantCount[i]+1] = mutantCounts[i];
    f = f / sum(f);
    f = f .* (1 + s * f);
    f[activeVariantCount[i]+1] = 0;
    f = f/sum(f);
    f = f * (1-delta);
    f[activeVariantCount[i]+1] = delta;
    vLogLikelihood[i] = multinomial_lpmf(countsTemp|f);
  }
}