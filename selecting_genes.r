library(dplyr)
library(stringr)

setwd("/Users/dimitri/Nextcloud/CESURE/Master 2/transcriptomics/data")

#recovering all the hypoxia genes
hypoxia_ma <- read.csv2(file = "microarrays_hypoxia.csv")
hypoxia_rnaseq <- read.csv(file = "rnaseq_hypoxia.csv",sep=";",row.names = NULL)%>% filter(str_starts(row.names,"C"))

#dataframe with the intersection of genes identified in both techniques
hypoxia_inter <- hypoxia_rnaseq%>%filter(row.names%in%rownames(hypoxia_ma)) %>% arrange(-log2FoldChange)

#create a rank for FC
hypoxia_inter <- hypoxia_inter %>% mutate(rank_FC=c(1:32))

#create a rank for adjpvalue
hypoxia_inter <- hypoxia_inter %>% arrange(padj)
hypoxia_inter <- hypoxia_inter %>% mutate(rank_padj=c(1:32))

#calculate the mean of the two ranks
hypoxia_inter$mean_rank <- (hypoxia_inter$rank_FC+hypoxia_inter$rank_padj)/2

#list of genes arranged by the new index
hypoxia_inter <- hypoxia_inter %>% arrange(mean_rank)
