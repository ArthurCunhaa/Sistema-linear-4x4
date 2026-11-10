from fractions import Fraction

VARIAVEIS = ["x", "y", "z", "w"]


def interpretar_termo(termo, n):
    if termo[-1] in VARIAVEIS[:n]:
        indice = VARIAVEIS.index(termo[-1])
        coef = termo[:-1]
        if coef == "":
            coef = "1"
        elif coef == "-":
            coef = "-1"
        return indice, Fraction(coef)
    return None, Fraction(termo)


def interpretar_equacao(linha, n):
    if "=" not in linha:
        valores = [Fraction(v) for v in linha.split()]
        if len(valores) != n + 1:
            raise ValueError
        return valores[:n], valores[n]

    esquerda, direita = linha.split("=")
    coefs = [Fraction(0)] * n
    constante = Fraction(0)

    s = esquerda.replace(" ", "").replace("*", "").replace("-", "+-")
    for termo in [p for p in s.split("+") if p]:
        indice, valor = interpretar_termo(termo, n)
        if indice is None:
            constante += valor
        else:
            coefs[indice] += valor

    termo_independente = Fraction(direita.strip()) - constante
    return coefs, termo_independente


def ler_sistema(n=4):
    print("Digite cada equação, uma por linha. Exemplos:")
    print("  2x + y - z + 3w = 8")
    print("  0 + y + z + w = 0")
    print("Também aceita só números: 2 1 -1 3 8")
    A, b = [], []
    for i in range(n):
        while True:
            try:
                linha = input(f"Equação {i + 1}: ").strip()
                coefs, termo = interpretar_equacao(linha, n)
                break
            except (ValueError, ZeroDivisionError):
                print("Entrada inválida. Use o formato 2x + y - z + 3w = 8 ou os 5 números separados por espaço.")
        A.append(coefs)
        b.append(termo)
    return A, b


def escalonar(M):
    M = [linha[:] for linha in M]
    n = len(M)
    det = Fraction(1)
    trocas = 0
    for col in range(n):
        pivo = next((r for r in range(col, n) if M[r][col] != 0), None)
        if pivo is None:
            return M, Fraction(0)
        if pivo != col:
            M[col], M[pivo] = M[pivo], M[col]
            trocas += 1
        det *= M[col][col]
        for r in range(col + 1, n):
            fator = M[r][col] / M[col][col]
            M[r] = [M[r][k] - fator * M[col][k] for k in range(len(M[r]))]
    if trocas % 2:
        det = -det
    return M, det


def inversa(A):
    n = len(A)
    M = [A[i][:] + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivo = next((r for r in range(col, n) if M[r][col] != 0), None)
        if pivo is None:
            return None
        M[col], M[pivo] = M[pivo], M[col]
        p = M[col][col]
        M[col] = [x / p for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][k] - f * M[col][k] for k in range(2 * n)]
    return [linha[n:] for linha in M]


def substituicao_regressiva(M):
    n = len(M)
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        soma = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][n] - soma) / M[i][i]
    return x


def imprimir(M, titulo=""):
    if titulo:
        print(f"\n{titulo}")
    for linha in M:
        print("  ".join(f"{str(v):>10}" for v in linha))


def main():
    A, b = ler_sistema()
    n = len(A)

    imprimir(A, "Matriz dos coeficientes A:")
    imprimir([[b[i]] for i in range(n)], "Vetor dos termos independentes b:")

    _, det = escalonar(A)
    print(f"\nDeterminante de A: {det}")
    if det == 0:
        print("\nA matriz é singular (det = 0). O sistema não tem solução única.")
        return

    aug = [A[i] + [b[i]] for i in range(n)]
    escalonada, _ = escalonar(aug)
    imprimir(escalonada, "Sistema escalonado [A | b]:")

    x = substituicao_regressiva(escalonada)

    inv = inversa(A)
    imprimir(inv, "Matriz inversa A^-1:")

    x_inv = [sum(inv[i][j] * b[j] for j in range(n)) for i in range(n)]

    print("\nSolução (escalonamento):")
    for i, v in enumerate(x, 1):
        print(f"  x{i} = {v}")

    print("\nSolução (A^-1 * b), para conferência:")
    for i, v in enumerate(x_inv, 1):
        print(f"  x{i} = {v}")

    residuo = [sum(A[i][j] * x[j] for j in range(n)) - b[i] for i in range(n)]
    print("\nVerificação A * x - b (deve ser tudo zero):", [str(r) for r in residuo])


if __name__ == "__main__":
    main()
