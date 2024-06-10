import math

def f(x):
    return (x**2)*math.sin(1/x**2)


def Calcular_erro_arredondamento(n, h, decimals):
    unidade_erro = 0.5 * 10 ** (-(decimals+1))
    total_erro_arredondamento = n * unidade_erro * h
    return round(total_erro_arredondamento, decimals)

def trapezio(a, b, n, decimals):
    #if a <= 0:
        #raise ValueError("O valor de 'a' deve ser maior que 0 para f(x) = log(x).")
    h = (b - a) / n
    x_valor = [a + i*h for i in range(n+1)]
    y_valor = [f(x) for x in x_valor]

    print("Intervalo, Valor de f(x)")
    for i in range(len(x_valor)):
        print(f"{x_valor[i]:.2f}, {y_valor[i]:.{decimals}f}")

    area = h * (0.5 * y_valor[0] + sum(y_valor[1:n]) + 0.5 * y_valor[n])
    area_arredondado = round(area, decimals)
    erro_arredondamento= Calcular_erro_arredondamento(n, h, decimals)

    min_area = round(area_arredondado - erro_arredondamento, decimals)
    max_area = round(area_arredondado + erro_arredondamento, decimals)

    print(f"\nSoma das áreas dos trapézios: {area_arredondado}")
    print(f"Erro de arredondamento estimado: {erro_arredondamento}")
    print(f"Com {n} trapézios e passo {h:.{decimals}f}")
    print(f"Intervalo de resposta: [{min_area}, {max_area}]")

    return area_arredondado, erro_arredondamento

# Exemplo de uso com log(x):
a = 1  # Início do intervalo de integração, deve ser maior que 0
b = 2  # Fim do intervalo de integração
n = 5  # Número de trapézios
decimals = 4  # Número de casas decimais

area, erro_arredondamento= trapezio(a, b, n, decimals)
