fConvertTime <- function(aDF_data){
  lTimeOld <- unique(aDF_data$generation)
  aTimeLookup <- data.frame(old=lTimeOld,new=seq_along(lTimeOld))
  aDF_copy <- aDF_data
  aDF_copy$generation <- aTimeLookup$new[match(aDF_copy$generation,aTimeLookup$old)]
  return(aDF_copy)
}

# Convert variants
fConvertVariants <- function(aDF_data){
  lVarOld <- unique(aDF_data$variant)
  aVarLookup <- data.frame(old=lVarOld,new=seq_along(lVarOld))
  aDF_copy <- aDF_data
  aDF_copy$variant <- aVarLookup$new[match(aDF_copy$variant,aVarLookup$old)]
  aDF_copy <- aDF_copy[order(aDF_copy$generation,aDF_copy$variant),]
  return(aDF_copy)
}

fGetVariantAppearance <- function(aDF_data){
  lVariant <- unique(aDF_data$variant)
  aFirstAppearanceDF <- data.frame(variant=lVariant,appearance=vector(length = length(lVariant)))
  for(i in seq_along(lVariant)){
    aTempDF <- aDF_data[aDF_data$variant==lVariant[i],]
    aFirstAppearanceDF$appearance[i] <- aTempDF$generation[1]
  }
  return(aFirstAppearanceDF)
}

fcountMutants <- function(aGeneration,aDF_data){
  lGens <- aGeneration:(aGeneration + 1)
  aDF_temp <- aDF_data[aDF_data$generation%in%lGens,]
  lVariant_1 <- aDF_temp$variant[aDF_temp$generation==aGeneration]
  lVariant_2 <- aDF_temp$variant[aDF_temp$generation==(aGeneration+1)]
  lMutantVariant <- setdiff(lVariant_2,lVariant_1)
  aMutantDF <- aDF_temp[aDF_temp$variant%in%lMutantVariant,]
  aCount <- sum(aMutantDF$count)
  # print(aCount)
  # stopifnot(all.equal(aMutantDF$count,rep(1,nrow(aMutantDF))))
  return(aCount)
}

fMutantCountsAll <- function(aDF_data){
  aLen <- length(unique(aDF_data$generation))
  lMutantCount <- vector(length=(aLen-1))
  for(i in 1:(aLen-1)){
    lMutantCount[i] <- fcountMutants(i,aDF_data)
  }
  return(lMutantCount)
}

## Create matrix of counts for variants (rows) and generations (cols)
fGetCounts <- function(aDF_short){
  aDF_short <- fConvertVariants(aDF_short)
  K <- length(unique(aDF_short$variant))
  N <- max(aDF_short$generation)
  mCounts <- matrix(nrow = K,ncol = N)
  for(i in 1:N){
    aTempDF <- aDF_short[aDF_short$generation==i,]
    for(j in 1:nrow(aTempDF)){
      mCounts[aTempDF$variant[j],i] <- aTempDF$count[j]
    }
  }
  mCounts[is.na(mCounts)] <- 0
  return(mCounts)
}

## Active variant count
fGetActiveVariantCount <- function(mCounts){
  N <- ncol(mCounts)
  lActiveCount <- vector(length=N)
  for(i in 1:N){
    lTemp <- mCounts[,i]
    lTemp <- which(lTemp!=0,arr.ind = T)
    lActiveCount[i] <- max(lTemp)
  }
  return(lActiveCount) 
}

fPrepareAll <- function(aDF_short){
  lMutantCount <- fMutantCountsAll(aDF_short)
  aFirstAppearances <- fGetVariantAppearance(aDF_short)
  mCounts <- fGetCounts(aDF_short)
  aDF_short <- fConvertTime(aDF_short)
  aDF_short <- fConvertVariants(aDF_short)
  K <- length(unique(aDF_short$variant))
  N <- max(aDF_short$generation)
  lActiveCount <- fGetActiveVariantCount(mCounts)
  data=list(N=N,K=K,firstAppearance=aFirstAppearances$appearance,
            mutantCounts=lMutantCount,
            counts=mCounts,
            activeVariantCount=lActiveCount)
  return(data)
}