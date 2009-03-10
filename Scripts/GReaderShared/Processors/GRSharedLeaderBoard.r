Sort <- function(frame, series)
{
	frame[order(series, decreasing=T),][,]
}

filepath <- commandArgs(trailingOnly=T)[2]
chartoutputpath <- paste(filepath,".png",sep="")

filepath

chartheight <- 500
chartwidth <- 703

data <- read.table(filepath,header=T)
data <- Sort(data, data$Shares)

total <- sum(data$Shares)

data <- data.frame(Site=data$Source, SharedStories=data$Shares, Percentage=paste(format(data$Shares/total*100,digits=3),"%"))

png(chartoutputpath,height=chartheight, width=chartwidth)
hist(data$SharedStories[-1], main=paste("Distribution of Shares per site for the last ",total - 1," shared stories"), xlab="Shares", ylab="No. of Sites", col=rgb(132,194,0,max=255),labels=T)
dev.off()

write.table(data, file=filepath, sep="\t")
