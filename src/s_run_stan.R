rm(list=ls())
setwd("~/Desktop/Selection_simulations/src")
library(rstan)
library(tidyverse)
options(mc.cores=4)
source("s_functions.R")

args <- commandArgs(trailingOnly=TRUE)
selection <- as.numeric(args[1])
a_break <- as.numeric(args[2])

d <- read.csv("../data/WF_generations4001_5000_allselectionlevels.csv", header=TRUE)
d <- filter(d, S==selection)

d$generation <- d$generation - min(d$generation) + 1
generations <- unique(d$generation)
log_min <- log10(min(generations))
log_max <- log10(max(generations))
log_uniform <- seq(log_min, log_max, length.out = 50)
breaks <- 10^(log_uniform)
breaks <- breaks[breaks >= 5]
saveRDS(breaks, "../data/inference/breaks.rds")
aDF_short <- subset(d, generation <= breaks[a_break])

aModel <- stan_model('multinomial_freqDep_homogeneous.stan')

initFn <- function(){
  list(s=0,
       delta=0.005)
}

data_stan <- fPrepareAll(aDF_short)
fit <- sampling(aModel,data=data_stan, iter=200, chains=4, init=initFn)
saveRDS(fit, file = paste0("../data/inference/WF_s_", selection, "_break_", a_break, ".rds"))