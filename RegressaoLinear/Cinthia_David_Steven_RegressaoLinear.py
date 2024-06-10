import tkinter as tk
from tkinter import messagebox, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class RegressaoLinear:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inserir Pares Ordenados")
        self.num_pares = 0
        self.valores = []
        self.entry_var_x = tk.StringVar()
        self.entry_var_y = tk.StringVar()
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.label1 = tk.Label(self.frame, text="Digite o número de pares ordenados:")
        self.label1.pack()
        self.entry1 = tk.Entry(self.frame)
        self.entry1.pack()
        self.label2 = tk.Label(self.frame, text="Digite o número de casas decimais para os resultados:")
        self.label2.pack()
        self.entry2 = tk.Entry(self.frame)
        self.entry2.pack()
        self.label3 = tk.Label(self.frame, text="Como deseja chamar as variáveis X e Y? (Opcional)")
        self.label3.pack()
        self.entry_x = tk.Entry(self.frame, textvariable=self.entry_var_x)
        self.entry_x.pack()
        self.entry_y = tk.Entry(self.frame, textvariable=self.entry_var_y)
        self.entry_y.pack()
        self.button = tk.Button(self.frame, text="Avançar", command=self.verificar_numero)
        self.button.pack()
        

    def verificar_numero(self):
        try:
            self.num_pares = int(self.entry1.get())
            self.num_casas_decimais = int(self.entry2.get())
            if self.num_pares > 0 and self.num_casas_decimais > 0:
                self.frame.destroy()
                self.criar_tabela()
            else:
                messagebox.showerror("Erro", "Por favor, insira um número positivo.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")

    def criar_tabela(self):
        self.root.title("Inserir Valores de X e Y")
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame_canvas = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_canvas, anchor=tk.NW)
        label_x = tk.Label(self.frame_canvas, text="X", font=font.Font(weight='bold', size=12))
        label_x.grid(row=0, column=3)
        label_y = tk.Label(self.frame_canvas, text="Y", font=font.Font(weight='bold', size=12))
        label_y.grid(row=0, column=6)
        self.valores_entries = []
        for i in range(self.num_pares):
            z = i + 1
            label_x = tk.Label(self.frame_canvas, text=f"X{z}: ")
            label_x.grid(row=z, column=2, padx=5, pady=5)
            entry_x = tk.Entry(self.frame_canvas)
            entry_x.grid(row=z, column=3, padx=5, pady=5)
            label_y = tk.Label(self.frame_canvas, text=f"Y{z}: ")
            label_y.grid(row=z, column=5, padx=5, pady=5)
            entry_y = tk.Entry(self.frame_canvas)
            entry_y.grid(row=z, column=6, padx=5, pady=5)
            self.valores_entries.append((entry_x, entry_y))
            
        self.frame.update_idletasks()  # Atualizar a geometria do frame dentro do canvas
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Atualizar a região rolável do canvas
        
        
        self.button_send = tk.Button(self.frame_canvas, text="Enviar", command=self.obter_valores)
        self.button_send.grid(row=self.num_pares+1, columnspan=7, rowspan=7, padx=5, pady=5)

    def obter_valores(self):
        self.valores_x = []
        self.valores_y = []
        self.pares_ordenados = []
        for entry_x, entry_y in self.valores_entries:
            try:
                valor_x = float(entry_x.get())
                valor_y = float(entry_y.get())
                self.pares_ordenados.append((valor_x, valor_y))
                self.valores_x.append(valor_x)
                self.valores_y.append(valor_y)
                entry_x.config(state='readonly', font=font.Font(weight='bold', size=12))
                entry_y.config(state='readonly', font=font.Font(weight='bold', size=12))
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores válidos para X e Y.")
                return
        
        self.button_send.destroy()
        self.executar_regressao()

    def valor_Y(self, valor_X=None):
        if valor_X is None:
            y = self.a + self.b * np.array(self.valores_x)
        else:
            y = self.a + self.b * valor_X
        return y

    def equacao_reta(self):
        return f"y = {self.a:{self.num_casas_decimais}} + {self.b:{self.num_casas_decimais}}x"

    def calcular_somas(self):
        self.n = len(self.valores_x)
        self.soma_X = np.sum(self.valores_x)
        self.soma_Y = np.sum(self.valores_y)
        self.soma_XY = np.sum(np.multiply(self.valores_x, self.valores_y))
        self.soma_X_quadrado = np.sum(np.square(self.valores_x)) 
        self.soma_Y_quadrado = np.sum(np.square(self.valores_y))
    
    def calcular_medias(self):
        self.media_X = self.soma_X / self.n
        self.media_Y = self.soma_Y / self.n
        self.media_XY = self.soma_XY / self.n
        self.media_X_quadrado = self.soma_X_quadrado / self.n
        self.media_Y_quadrado = self.soma_Y_quadrado / self.n
    def calcular_coeficientes_reta(self):
        
        b = round((self.n * self.soma_XY - self.soma_X * self.soma_Y) / (self.n * self.soma_X_quadrado - self.soma_X**2), self.num_casas_decimais)
        a = round((self.soma_Y - self.soma_X * b)/self.n, self.num_casas_decimais)
        
        return a, b

    def calcular_coeficiente_determinacao(self):
        correlacao = self.calcular_coeficiente_correlacao()
        coef_determinacao = (correlacao**2) * 100
        return coef_determinacao 
    
    def calcular_coeficiente_correlacao(self):
        
        Cov_xy = self.media_XY - (self.media_X * self.media_Y)
        
        desvio_padrao_X = np.sqrt(self.media_X_quadrado - self.media_X**2)
        desvio_padrao_Y = np.sqrt(self.media_Y_quadrado - self.media_Y**2) 
        
        r = Cov_xy / (desvio_padrao_X * desvio_padrao_Y)
        return r
        
    def criar_grafico(self):
        
        self.root.update_idletasks()  # Atualiza a geometria da janela
        
        # Adiciona barra de rolagem à janela
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        label_texto = tk.Label(self.frame_canvas, text=self.texto_resposta)
        label_texto.config(font=font.Font(size=14))
        label_texto.grid(row=1, column=9, columnspan=8, padx=5, pady=5)
        
        label_valor_x = tk.Label(self.frame_canvas, text="Digite o valor de X para calcular o valor de Y: ")
        label_valor_x.config(font=font.Font(size=14))
        label_valor_x.grid(row=2, column=9, padx=5, pady=5)
        
        entry_valor_x = tk.Entry(self.frame_canvas, textvariable=self.entry_var_x)
        entry_valor_x.grid(row=2, column=10, columnspan=3, padx=5, pady=5)
        
        self.fig, self.grafico = plt.subplots()
        self.grafico.scatter(self.valores_x, self.valores_y, color='blue', label='Dados')
        # Exemplo de valores para y
        
        self.grafico.plot(self.valores_x, self.valor_Y(), color='red', label='Reta de Regressão')

        self.grafico.set_xlabel(self.entry_var_x.get() if self.entry_var_x.get() else "X")
        self.grafico.set_ylabel(self.entry_var_y.get() if self.entry_var_y.get() else "Y")
        self.grafico.set_title("Gráfico de Dispersão")
        
        self.button_valor_y = tk.Button(self.frame_canvas, text="Calcular", command=self.calcular_y)
        self.button_valor_y.grid(row=2, column=13, padx=5, pady=5)
        
        self.canvas_fig = FigureCanvasTkAgg(self.fig, master=self.frame_canvas)
        self.canvas_fig.draw()
        self.canvas_fig.get_tk_widget().grid(row=self.num_pares+2, columnspan=7, padx=5, pady=5)
        
        self.frame_canvas.update_idletasks()  # Atualizar a geometria do frame dentro do canvas
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Atualizar a região rolável do canvas
        

    def executar_regressao(self):
        self.calcular_somas()
        self.calcular_medias()
        coef_correlacao = self.calcular_coeficiente_correlacao()
        coef_determinacao = self.calcular_coeficiente_determinacao()
        self.a, self.b = self.calcular_coeficientes_reta()
        eq_reta = self.equacao_reta()
        
        self.texto_resposta = "Coeficiente de Correlação de Person: " + f"{round(coef_correlacao, self.num_casas_decimais)}" + "\n"
        self.texto_resposta += "Coeficiente de Determinação (%): " + f"{round(coef_determinacao, 2)}" + "\n"
        self.texto_resposta += "Equação da Reta de Regressão: " + eq_reta + "\n"
        
        self.criar_grafico()
        
    def calcular_y(self):
        try:
            valor_X = float(self.entry_var_x.get())
            valor_Y_especifico = self.valor_Y(valor_X)
            self.texto_resposta_y = f"Valor de Y para X = {valor_X}: " + f"{round(valor_Y_especifico, self.num_casas_decimais)}" + "\n"
            label_texto_y = tk.Label(self.frame_canvas, text=self.texto_resposta_y)
            label_texto_y.config(font=font.Font(size=14))
            label_texto_y.grid(row=4, column=9, padx=5, pady=5)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor válido para X.")

if __name__ == "__main__":
    interface = RegressaoLinear()
    interface.root.mainloop()
