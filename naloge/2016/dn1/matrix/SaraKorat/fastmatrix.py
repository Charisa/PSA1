# -*- coding: utf-8 -*-
from slowmatrix import SlowMatrix

class FastMatrix(SlowMatrix):
    """
    Matrika z množenjem s Strassenovim algoritmom.
    """
    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Množenje izvede s Strassenovim algoritmom.
        """
        assert left.ncol() == right.nrow(), \
               "Dimenzije matrik ne dopuščajo množenja!"
        assert self.nrow() == left.nrow() and right.ncol() == self.ncol(), \
               "Dimenzije ciljne matrike ne ustrezajo dimenzijam produkta!"
        # raise NotImplementedError("Naredi sam!")



        # Vrednosti dimenzij shranimo v nove spremenljivke, torej je po novih spremenljivkah
        # leva matrika dimenzije n x m in desna matrika dimenzije m x k.

        n = left.nrow()             
        m = left.ncol() # = right.nrow()
        k = right.ncol()

        # Definiramo nove spremenljivke, ki (sicer zanemarljivo) zmanjšajo število operacij

        N = n//2
        M = m//2
        K = k//2
        N2 = 2 * N
        M2 = 2 * M
        K2 = 2 * K
        

        # Če je ena od dimenzij matrik enaka 1, imamo navadno množenje - SlowMatrix; množenje podedujemo iz SlowMatrix.

        if n == 1 or m == 1 or k == 1:
            super().multiply(left, right)        

        else:

            # Definiramo podmatrike za Strassenov algoritem

            A = left[0:N, 0:M]
            B = left[0:N, M:M2]                        # V primeru, da je left.ncol() liho število, gremo do vključno predzadnjega stolpca.
            C = left[N:N2, 0:M]                        # Isto kot pri lihih stolpcih, s tem da sedaj lihe vrstice.
            D = left[N:N2, M:M2]                       # Pri D pazimo na lihe vrstice in lihe stolpce.
                                                       # Podobno naredimo še za desno matriko.
            E = right[0:M, 0:K]
            F = right[0:M, K:K2]
            G = right[M:M2, 0:K]
            H = right[M:M2, K:K2]

            print("A " +  str(A), "F " + str(F), "H " + str(H))

            # Produkti za računanje algoritma

            P1 = A * (F - H)
            P2 = (A + B) * H
            P3 = (C + D) * E
            P4 = D * (G - E)
            P5 = (A + D) * (E + H)
            P6 = (B - D) * (G + H)
            P7 = (A - C) * (E + F)


            # Primer, ko so vse dimenzije sode:

            self[0:N, 0:K] = P4 + P5 + P6 - P2
            self[0:N, K:K2] = P1 + P2
            self[N:N2, 0:K] = P3 + P4
            self[N:N2, K:K2] = P1 + P5 - P3 - P7



            # Če je m lihe dimenzije:
            if m % 2 != 0:
                for i in range(n):
                    for j in range(k):
                        self[i, j] += left[i, m - 1] * right[m - 1, j]              # [i,j]-temu elementu matrike self prištejemo še zmnožek 
                # Če sta m in k lihe dimenzije:
                if k % 2 != 0:
                    self[0:n, k - 1] = left * right[0:m, k - 1]                     # Novi matriki dodamo še stolpec
                    # Če so m, k in n lihe dimenzije:
                    if n % 2 != 0:
                        self[n - 1, 0:k] = left[n - 1, 0:m] * right                 # Novi matriki dodamo vrstico                      
                # Če sta m in n lihe, k pa sode dimenzije:
                else:
                    if n % 2 != 0:
                        self[n-1, 0:k] = left[n - 1, 0:m] * right                   # Novi matriki dodamo vrstico
            # Če je m sode dimenzije:
            else:
                # Če je m sode in k lihe dimenzije:
                if k % 2 != 0:
                    self[0:n, k - 1] = left * right[0:m, k-1]                       # Novi matriki dodamo stolpec
                    # Če je m sode, k in n pa lihe dimenzije:
                    if n % 2 != 0:
                        self[n-1, 0:k] = left[n - 1, 0:m] * right                   # Novi matriki dodamo vrstico 
                # Če sta m in k sode, n pa lihe stopnje:
                else:
                    self[n-1, 0:k] = left[n - 1, 0:m] * right                       # Novi matriki dodamo vrstico 
                        
               

            # Ne dela: Error: dimenzije se ne ujemajo!       
