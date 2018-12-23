## Python model generated way that frequency affects probability

logistic <- function(x){
  return(1 / (1 + exp(-x)))
}

logit <- function(x){
  return(log(x / (1 - x)))
}

curve(logistic(x), -10, 10)
curve(logit(x), 0, 1)

logistic_probability <- function(mu, beta, f){
  return(logistic(logit(1 - mu) + beta * f))
}

mu <- 0.005
# neutral
curve(logistic_probability(mu, 0, x), 0, 1)

# negative frequency dependence
curve(logistic_probability(mu, -10, x), 0, 1)

# positive frequency dependence -- EFFECT IS TINY!
curve(logistic_probability(mu, 10, x), 0, 1)

# relative selection in a given generation
s <- function(aBeta, p_g1, p_g2){
  return((1 + aBeta * p_g1) / (1 + aBeta * p_g2) - 1)
}

curve(s(1, x, 0.1), 0, 1)
curve(s(-1, x, 0.1), 0, 1)

