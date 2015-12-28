
# plot.R datafile picture_file
# Rscript plot.R data1.csv plot1.png

args <- commandArgs(trailingOnly = TRUE)

png(file = args[2], bg = "transparent")

d = read.table(args[1], sep=',', na.strings="*", header=F)
# y = d[2, 4:49]
# f = d[1, 4:49]

y = d[2, 4:48]
f1 = d[1, 4:48]


M = max(cbind(y, f1), na.rm=T)
M = max(M, 100)
m = min(cbind(y, f1), na.rm=T)
m = min(m, 0)

plot(1:45, y, xlab='time', ylab='data', ylim=c(m, M))
lines(1:45, f1)
legend('topleft', c('point == MODIS', 'FILTER1'), lty=c(0, 1))

dev.off()
