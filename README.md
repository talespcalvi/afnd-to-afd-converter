# Conversor de AFND (com movimentos vazios) para AFD

## AFND
![AFND](https://github.com/talespcalvi/afnd-to-afd-converter/blob/main/afnd.jpg)

### Entrada utilizada
##### A B C D
##### A 
##### D
##### A 1 B
##### A 0 C
##### A h C
##### A h D
##### B 1 B
##### B 0 C
##### C 1 A
##### C h D
##### D 0 D


## AFD
![AFD](https://github.com/talespcalvi/afnd-to-afd-converter/blob/main/afd.jpg)

### Saída Gerada
##### Q0 Q1 Q2 Q3
##### Q0
##### Q0 Q1 Q2 Q3
##### Q0 0 Q1
##### Q0 1 Q2
##### Q1 0 Q3
##### Q1 1 Q0
##### Q2 0 Q1
##### Q2 1 Q2
##### Q3 0 Q3


# Checagem se a palavra é reconhecida ou não pelo AFD

## Entrada
##### 010
##### 111
##### 00111
##### 0111
##### 101011
##### 101
##### 101
##### 11

## Saída
##### 010 aceito
##### 111 aceito
##### 00111 n�o aceito
##### 0111 aceito
##### 101011 aceito
##### 101 aceito
##### 101 aceito
##### 11 aceito
