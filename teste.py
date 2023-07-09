# from random import randint
# tabuleiro = []

# def restantes(lista):
#     completa = [1,2,3,4,5,6,7,8,9]
#     resta = []
#     for x in completa:
#         if x not in lista:
#             resta.append(x)
#     return resta

# def contem(lista1,lista2):
#     for x in lista1:
#         if x not in lista2:
#             return False
#     return True


# n_linha=0
# while n_linha<9:
#     cont = 0
#     linha = []
#     flag = False
#     while cont<9:
#         nums_col = []
#         num = randint(1,9)
#         flag = False
#         if num not in linha:
#             i = n_linha-1
#             while i>=0:
#                 nums_col.append(tabuleiro[i][cont])
#                 i-=1

#             resta = restantes(linha)
#             if contem(resta,nums_col) :
#                 tabuleiro= []
#                 flag=True
#                 n_linha = 0
#                 break
#             if num not in nums_col:
#                 linha.append(num)
#                 cont+=1
            
#     if not flag:
#         tabuleiro.append(linha)
#         n_linha+=1

# for _ in tabuleiro:
#     print(_)


# x = [[],[],[],[],[],[],[],[],[]]

# for i in range(9):
#     for j in range(9):
#         x[i].append(j+(i*9))

# for item in x:
#     print(item)

# for i in range(9):
#     if 5 in x[i]:
#         j= x[i].index(5)
#         break

# print((i,j))

print(1 == '1')