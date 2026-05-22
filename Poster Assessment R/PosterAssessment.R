
################################################
#ICC Analysis
################################################
library(psych)
library (irr)


# Genes count
genes <- read.csv("Genes.csv", row.names = 1)
ICC_genes<-ICC(genes)
ICC_genes<-ICC_genes$results
write.csv(ICC_genes,"ICC_genes.csv")

# Major genes count
major_genes <- read.csv("Major_Genes.csv", row.names = 1)
ICC_major_genes<-ICC(major_genes)
ICC_major_genes<-ICC_major_genes$results
write.csv(ICC_major_genes,"ICC_major_genes.csv")

# Databases count
databases <- read.csv("Databases.csv", row.names = 1)
ICC_databases<-ICC(databases)
ICC_databases<-ICC_databases$results
write.csv(ICC_databases,"ICC_databases.csv")

# Figures count
figures <- read.csv("Figures.csv", row.names = 1)
ICC_figures<-ICC(figures)
ICC_figures<-ICC_figures$results
write.csv(ICC_figures,"ICC_figures.csv")

ocr1.1<-read.csv("OCR1.1_R.csv", row.names = 1)
kappam.fleiss(ocr1.1)

################################################
#Plots
################################################
library(ggplot2)
library(dplyr)

##### Database Presence  ################################################################################

database_presence <- read.csv("Database_presence.csv")
database_order<-c("FlyBase", "HPA","KEGG","MGI", "PubMed","EbscoHost","NCBI","Google Scholar", "ResearchGate", "CellxGene")
Scorer_order<-c("SY", "LS", "FT")
database_presence$Database <- factor(database_presence$Database, levels = database_order)
database_presence$Scorer <- factor(database_presence$Scorer, levels = Scorer_order)

database_presence_means <- database_presence %>%
  group_by(Database) %>%
  summarise(Mean_Score = mean(Score, na.rm = TRUE), StDev = sd(Score))

#Grouped bar plot (by individual scorer)
ggplot(database_presence, aes(fill=Scorer, y=Score, x=Database)) + 
  geom_bar(position="dodge", stat="identity") +
  theme_bw()
#Mean bar plot (Mean across scorers with standard deviation)
ggplot(database_presence_means, aes(y=Mean_Score, x=Database)) + 
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin = Mean_Score - StDev, ymax = Mean_Score + StDev), width = 0.2)+
  theme_bw()

##### Figure presence ################################################################################


figure_presence <- read.csv("Figure_presence.csv")
Figure_order<-c("Bar", "Dot","Pathway","Network", "Line","Heatmap","scRNA","Interaction", "Other")
Scorer_order<-c("SY", "LS", "FT")
figure_presence$Figure <- factor(figure_presence$Figure, levels = Figure_order)
figure_presence$Scorer <- factor(figure_presence$Scorer, levels = Scorer_order)

figure_presence_means <- figure_presence %>%
  group_by(Figure) %>%
  summarise(Mean_Score = mean(Score, na.rm = TRUE), StDev = sd(Score))


#Grouped bar plot (by individual scorer)
ggplot(figure_presence, aes(fill=Scorer, y=Score, x=Figure)) + 
  geom_bar(position="dodge", stat="identity") +
  theme_bw()

#Mean bar plot (Mean across scorers with standard deviation)
ggplot(figure_presence_means, aes(y=Mean_Score, x=Figure)) + 
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin = Mean_Score - StDev, ymax = Mean_Score + StDev), width = 0.2)+
  theme_bw()

##### Genes counts ################################################################################


genes_R <- read.csv("Genes_R.csv")
Scorer_order<-c("SY", "LS", "FT")
genes_R$Scorer <- factor(genes_R$Scorer, levels = Scorer_order)

ggplot(genes_R, aes(fill=Scorer, y=Avg, x=Category)) + 
  geom_bar(stat="identity", position = position_dodge(width = 0.9)) +
  geom_errorbar(aes(ymin = Avg - Stdev, ymax = Avg + Stdev), width = 0.2, position = position_dodge(width = 0.9))+
  theme_bw()



















#Library IRR tried but not preferred 
library(irr)

icc(genes, model = "mixed",
    type = "agreement", unit = "average")
