rm(list=ls())
library(ggplot2)
setwd("~/Desktop/Selection_simulations")
aDF <- read.csv('./Results/testFreqMean12_0.csv',header = F)
# aMax = max(aDF$V2)
# aUpper = log(aMax)/log(10)*2
# lBreaks <- sapply(0:11,function(i) 10^(0.5*i))
# aTest <- hist(aDF$V2,breaks = lBreaks)
# 
# aShortDF <- data.frame(proportion=aTest$counts/nrow(aDF),numCopies=aTest$breaks[-1])
# ggplot(aShortDF,aes(x=numCopies,y=proportion)) + geom_point() + scale_x_log10() + scale_y_log10() +
#   geom_smooth()

fImport <- function(aName,i,j){
  aFilename <- paste0(aName,i,"_",j,".csv")
  aDF <- read.csv(aFilename,header = F)
  lBreaks <- sapply(0:11,function(i) 10^(0.5*i))
  aTest <- hist(aDF$V2,breaks = lBreaks)
  aShortDF <- data.frame(proportion=aTest$counts/nrow(aDF),numCopies=aTest$breaks[-1])
  return(aShortDF)
}

fImportAndAverage <- function(aName,i,aMaxIter){
  for(j in 0:(aMaxIter-1)){
    print(j)
    aTest <- fImport(aName,i,j)
    if(j == 0){
      aOverall <- aTest
    } else{
      aOverall$proportion <- aOverall$proportion + aTest$proportion
    }
  }
  aOverall$proportion <- aOverall$proportion / aMaxIter
  return(aOverall)
}

vMu = c(0.004,0.008,0.016,0.032,0.064,0.128)
jMax <- 20
for(i in 1:6){
  aTempDF <- fImportAndAverage("./Results/testFreqMean",(i-1),jMax)
  aTempDF$number <- rep(vMu[i],nrow(aTempDF))
  if(i == 1){
    aBigDF <- aTempDF
  }else{
    aBigDF <- rbind.data.frame(aBigDF,aTempDF)
  }
}
aBigDF_positive <- aBigDF
for(i in 1:6){
  aTempDF <- fImportAndAverage("./Results/testFreqMean",(i+5),jMax)
  aTempDF$number <- rep(vMu[i],nrow(aTempDF))
  if(i == 1){
    aBigDF <- aTempDF
  }else{
    aBigDF <- rbind.data.frame(aBigDF,aTempDF)
  }
}
aBigDF_negative <- aBigDF
for(i in 1:6){
  aTempDF <- fImportAndAverage("./Results/testFreqMean",(i+11),jMax)
  aTempDF$number <- rep(vMu[i],nrow(aTempDF))
  if(i == 1){
    aBigDF <- aTempDF
  }else{
    aBigDF <- rbind.data.frame(aBigDF,aTempDF)
  }
}
aBigDF_null <- aBigDF






multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

aMin <- 10^(-5)
g1<- ggplot(aBigDF_negative,aes(x=numCopies,y=proportion,colour=as.factor(number))) + geom_point() + scale_x_log10(limits=c(1,1e5)) + scale_y_log10(limits=c(aMin,1)) + 
  geom_smooth(se=F) + xlab('number of copies of variant') + ylab('proportion') + labs(colour='mutation rate') + ggtitle('negative frequency dependent selection')

g2 <- ggplot(aBigDF_positive,aes(x=numCopies,y=proportion,colour=as.factor(number))) + geom_point() + scale_x_log10(limits=c(1,1e5)) + scale_y_log10(limits=c(aMin,1)) + 
  geom_smooth(se=F) + xlab('number of copies of variant') + ylab('proportion') + labs(colour='mutation rate') + ggtitle('positive frequency dependent selection')

g3 <- ggplot(aBigDF_null,aes(x=numCopies,y=proportion,colour=as.factor(number))) + geom_point() + scale_x_log10(limits=c(1,1e5)) + scale_y_log10(limits=c(aMin,1)) + 
  geom_smooth(se=F) + xlab('number of copies of variant') + ylab('proportion') + labs(colour='mutation rate') + ggtitle('neutral')

pdf(file = "frequency_dependent.pdf", width = 10, height = 8)
multiplot(g2,g3,g1, cols=1)
dev.off()

