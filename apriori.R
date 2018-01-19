library(arules)
library(arulesCBA)
library(foreign)

setwd("C:/Users/Yusuf/PycharmProjects/AssociationRule")

#For all binary EVs and CV
#data= read.csv("aprioriAllBinary.csv")
#View(data)

#For all categorical EVs and binary CV
data= read.csv("aprioriNonBinary.csv")
View(data)

#readFile <- read.delim("updatedAprioriSheet.dat", header = TRUE, sep = "", as.is = TRUE)

rules <- apriori(data, parameter = list(supp = 0.1, conf = 0.9, target = "rules"))

#rules <- apriori(data, parameter = list(support = 0.1, confidence = 0.80), appearance = list(rhs = c("percentChange=Up","percentChange=Down"), default = "lhs"))


rules.sorted <- sort(rules, by = "lift")


top10.rules <- head(rules.sorted, 10)
as(top10.rules, "data.frame")

