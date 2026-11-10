# Sistema Linear 4x4

Programa em Python que resolve sistemas lineares 4x4 digitados pelo usuário.

## Recursos

- Leitura das equações no formato algébrico, como `2x + y - z + 3w = 8`
- Eliminação de Gauss com pivoteamento parcial (escalonamento)
- Cálculo da matriz inversa pelo método de Gauss-Jordan
- Cálculo do determinante
- Solução por escalonamento e por A^-1 · b, com verificação do resultado
- Aritmética exata com `fractions.Fraction`, aceitando frações como `1/3`

## Requisitos

- Python 3.8 ou superior (não usa bibliotecas externas)

## Como usar

```bash
python main.py
```

Digite cada equação em uma linha, do jeito que escreve no papel. As variáveis são x, y, z e w, nessa ordem.

```
2x + y - z + 3w = 8
0 + y + z + w = 0
1/2x - 3z = 4
```

Termos que faltam são tratados como zero, e coeficientes 1 ou -1 podem ser escritos sem número (`x`, `-y`). Também é aceito o formato só com números: quatro coeficientes e o termo independente, separados por espaço. Para a primeira equação, `2 1 -1 3 8`.

Se o determinante for zero, o programa informa que o sistema não tem solução única.
