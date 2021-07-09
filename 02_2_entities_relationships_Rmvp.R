# Libraries
library(magrittr)
library(tidyverse)
library(viridis)
library(patchwork)
library(hrbrthemes)
library(igraph)
library(ggraph)
library(colormap)
library(dplyr)
library(stringr)


df <- read.csv("data/noticias_filtradas_entidades_nombresNormalizados.csv")
df %<>%
  mutate(X0 = if_else(str_length(X0)>1,X0, NULL),
         X1 = if_else(str_length(X1)>1,X1, NULL),
         X2 = if_else(str_length(X2)>1,X2, NULL),
         X3 = if_else(str_length(X3)>1,X3, NULL),
         X4 = if_else(str_length(X4)>1,X4, NULL))
nodos <- c()

#Recorre cada fila
for (i in 1:nrow(df[,8:12])){
  #Recorre cada uno de las columnas
  for (j in 1:5){
    if (is.na(df[i,8:12][1,j])==FALSE){
      nodos <- append(df[i,8:12][1,j], nodos)
    }
  }
}
nodos <- unique(nodos)
nodos
edges <- data.frame()

datos <- df[,8:12]

for (i in 1:nrow(datos)){ #Recorre cada fila
  print(i)
  lista <- c()
  for (l in 1:5){
    lista <- na.exclude(append(lista, datos[i,1:5][1,l]))
    if (length(lista)>1){
      for (v in 1:length(lista)){
        from <- lista[v]
        for (t in 1:length(setdiff(lista, from))){
          to <- setdiff(lista, from)[t]
          agregar <- data.frame("from"= from, 
                                "to" = to)
          edges <- rbind(edges, agregar)
          }
        }
    }
  }
}

edges <- distinct(edges)


# Transform to a igraph object
mygraph <- graph_from_data_frame(edges)

# Make the usual network diagram
p1 <-  ggraph(mygraph) + 
  geom_edge_link(edge_colour="black", edge_alpha=0.3, edge_width=0.2) +
  geom_node_point( color="#69b3a2", size=5) +
  geom_node_text( aes(label=name), repel = TRUE, size=8, color="#69b3a2") +
  theme_void() +
  theme(
    legend.position="none",
    plot.margin=unit(rep(2,4), "cm")
  ) 
p1
# Make a cord diagram
p2 <-  ggraph(mygraph, layout="linear") + 
  geom_edge_arc(edge_colour="black", edge_alpha=0.3, edge_width=0.2) +
  geom_node_point( color="#69b3a2", size=2.5) +
  geom_node_text( aes(label=name), repel = FALSE, size=5, color="#69b3a2", nudge_x =.5, nudge_y=-.5) +
  theme_void() +
  theme(
    legend.position="none",
    plot.margin=unit(rep(2,4), "cm")
  ) 


p2

