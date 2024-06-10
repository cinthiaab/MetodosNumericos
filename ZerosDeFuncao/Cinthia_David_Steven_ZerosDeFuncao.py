import tkinter as tk
from tkinter import messagebox, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import * 


class ZeroDaFuncao:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Programa Zeros de Função")
        self.num_pares = 0
        self.valores = []
        self.entry_var_x = tk.StringVar()
        self.entry_var_y = tk.StringVar()
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.label1 = tk.Label(self.frame, text="Digite a função: f(x) =")
        self.label1.pack()
        self.entry1 = tk.Entry(self.frame)
        self.entry1.pack()
        self.label2 = tk.Label(self.frame, text="Digite o intervalo de reta: [a, b]")
        self.label2.pack()
        self.entry2 = tk.Entry(self.frame)
        self.entry2.pack()
        self.label4 = tk.Label(self.frame, text="Digite o número de casas decimais para os resultados:")
        self.label4.pack()
        self.entry4 = tk.Entry(self.frame)
        self.entry4.pack()
        self.label3 = tk.Label(self.frame, text="Limite para o erro: |e|")
        self.label3.pack()
        self.entry3 = tk.Entry(self.frame)
        self.entry3.pack()
        self.button = tk.Button(self.frame, text="Avançar", command=self.verificar_numero)
        self.button.pack()
    
    def ler_entrada(self, valor):
        
        valor = float(valor)
        return valor

    def verificar_numero(self):
        try:
            self.num_casas_decimais = int(self.entry4.get()) # Número de casas decimais
            self.a, self.b = self.entry2.get().split(", ")  # Separa os valores de a e b e converte para float
            self.a_entrada = self.ler_entrada(self.a)
            self.b_entrada = self.ler_entrada(self.b)
            self.funcao = self.entry1.get()  # Função
            self.funcao = sympify(self.funcao)
            self.erro_limite = float(self.entry3.get())  # Erro
            
            if self.num_casas_decimais > 0:
                self.frame.destroy()
                self.calculando_zeros_da_funcao() # Chama a função para calcular os zeros da função
            else:
                messagebox.showerror("Erro", "Por favor, insira um número positivo.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")
            
    def calcular_sinal(self, result):
        if result > 0:
            comp =  '> 0 (positivo)'
        elif result < 0:
            comp = '< 0 (negativo)'
        else:
            comp = '= 0 (nulo)'
        return comp
    
    
    

    def calcular_erro(self, a, b):
        self.X0 = (a + b) / 2 # ponto médio do intervalo dado
        f_A = self.funcao.subs('x', a)
        f_X0 = self.funcao.subs('x', self.X0)
        f_B = self.funcao.subs('x', b)
        texto_resposta = f"{self.i}ª estimativa: \n"
        texto_resposta_estimativa = f"f({a}) = {round(f_A, self.num_casas_decimais)} {self.calcular_sinal(f_A)} \n"
        texto_resposta_estimativa += f"f({self.X0}) = {round(f_X0, self.num_casas_decimais)} {self.calcular_sinal(f_X0)}\n"
        texto_resposta_estimativa += f"f({b}) = {round(f_B, self.num_casas_decimais)} {self.calcular_sinal(f_B)}\n"
        
        self.estimativas.append(texto_resposta_estimativa)
        texto_resposta += texto_resposta_estimativa 
        
        
        if self.calcular_sinal(f_A) == self.calcular_sinal(f_X0):
            self.a_global = self.X0
            self.b_global = b
        else:
            self.a_global = a
            self.b_global = self.X0
        
        erro_calculado = (b-a)/2
        
        texto_resposta += f"X0 = {a} + {b} / 2 = {self.X0:.{self.num_casas_decimais}f} \n |e| <= {erro_calculado:.{self.num_casas_decimais}f}"
        print(texto_resposta)   
        return erro_calculado
    
    def calculando_zeros_da_funcao(self):
        self.i = 1
        self.estimativas = []
        erro_calculado = self.calcular_erro(self.a_entrada, self.b_entrada)
        
        
        while erro_calculado > self.erro_limite: 
            self.i += 1
            erro_calculado = self.calcular_erro(self.a_global, self.b_global)
            


if __name__ == "__main__":
    interface = ZeroDaFuncao()
    interface.root.mainloop()
