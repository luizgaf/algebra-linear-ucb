import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class SistemaLinearApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Sistemas Lineares")
        self.root.geometry("900x850")
        
        # Variáveis
        self.tamanho = tk.IntVar(value=2)
        self.mostrar_resolucao = tk.BooleanVar(value=False)
        self.matriz_entries = []
        self.vetor_entries = []
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="CALCULADORA DE SISTEMAS LINEARES", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Seção de configuração
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuração do Sistema", padding="10")
        config_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        ttk.Label(config_frame, text="Tamanho do sistema:").grid(row=0, column=0, sticky=tk.W)
        
        tamanho_frame = ttk.Frame(config_frame)
        tamanho_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        for i, valor in enumerate([2, 3, 4]):
            rb = ttk.Radiobutton(tamanho_frame, text=f"{valor}x{valor}", 
                               variable=self.tamanho, value=valor,
                               command=self.atualizar_interface)
            rb.grid(row=0, column=i, padx=(0, 20))
        
        # Botão para gerar campos
        ttk.Button(config_frame, text="🔄 Gerar Campos", 
                  command=self.gerar_campos).grid(row=0, column=3, padx=(20, 0))
        
        # Checkbox para mostrar resolução
        ttk.Checkbutton(config_frame, text="Mostrar resolução passo a passo",
                       variable=self.mostrar_resolucao).grid(row=1, column=0, columnspan=4, pady=(10, 0), sticky=tk.W)
        
        # Frame para matriz e vetor
        self.sistema_frame = ttk.LabelFrame(main_frame, text="Sistema Linear", padding="15")
        self.sistema_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Frame de exemplos
        exemplos_frame = ttk.LabelFrame(main_frame, text="Exemplos Prontos", padding="10")
        exemplos_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(exemplos_frame, text="Exemplo 2x2", 
                  command=self.exemplo_2x2).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(exemplos_frame, text="Exemplo 3x3", 
                  command=self.exemplo_3x3).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(exemplos_frame, text="Exemplo 4x4", 
                  command=self.exemplo_4x4).pack(side=tk.LEFT)
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        resultados_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        # Text area para resultados
        self.text_resultados = scrolledtext.ScrolledText(resultados_frame, width=90, height=18, 
                                                        font=('Consolas', 10), bg='#f8f9fa')
        self.text_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.grid(row=5, column=0, columnspan=4, pady=15)
        
        ttk.Button(botoes_frame, text="🚀 Resolver Sistema", 
                  command=self.resolver_sistema, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(botoes_frame, text="🗑️ Limpar Tudo", 
                  command=self.limpar_tudo).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(botoes_frame, text="📤 Copiar Resultados", 
                  command=self.copiar_resultados).pack(side=tk.LEFT)
        
        # Configurar weights para expansão
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=2)
        
        # Gerar campos iniciais
        self.gerar_campos()
    
    def gerar_campos(self):
        # Limpar campos existentes
        for widget in self.sistema_frame.winfo_children():
            widget.destroy()
        
        n = self.tamanho.get()
        self.matriz_entries = []
        self.vetor_entries = []
        
        # Títulos
        ttk.Label(self.sistema_frame, text="Matriz A (coeficientes):", 
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, columnspan=n, pady=(0, 8))
        ttk.Label(self.sistema_frame, text="Vetor b (constantes):", 
                 font=('Arial', 9, 'bold')).grid(row=0, column=n+1, columnspan=2, pady=(0, 8))
        
        # Criar entradas para a matriz com labels das variáveis
        for i in range(n):
            # Label da equação
            ttk.Label(self.sistema_frame, text=f"Eq {i+1}:", 
                     font=('Arial', 9, 'bold')).grid(row=i+1, column=0, padx=(0, 10), sticky=tk.E)
            
            linha_entries = []
            for j in range(n):
                frame_celula = ttk.Frame(self.sistema_frame)
                frame_celula.grid(row=i+1, column=j+1, padx=3, pady=3)
                
                ttk.Label(frame_celula, text=f"x{j+1}:").pack(side=tk.TOP)
                entry = ttk.Entry(frame_celula, width=6, font=('Arial', 10), justify='center')
                entry.pack(side=tk.TOP)
                linha_entries.append(entry)
            
            self.matriz_entries.append(linha_entries)
            
            # Sinal de igual
            ttk.Label(self.sistema_frame, text="=", font=('Arial', 12, 'bold')).grid(
                row=i+1, column=n+1, padx=10)
            
            # Entrada para o vetor
            frame_constante = ttk.Frame(self.sistema_frame)
            frame_constante.grid(row=i+1, column=n+2, padx=5, pady=3)
            
            entry_b = ttk.Entry(frame_constante, width=8, font=('Arial', 10, 'bold'), 
                               justify='center', style='Constante.TEntry')
            entry_b.pack()
            self.vetor_entries.append(entry_b)
    
    def atualizar_interface(self):
        self.gerar_campos()
    
    def obter_sistema(self):
        n = self.tamanho.get()
        matriz = np.zeros((n, n))
        vetor = np.zeros(n)
        
        try:
            for i in range(n):
                for j in range(n):
                    valor = self.matriz_entries[i][j].get().strip()
                    if valor == "":
                        raise ValueError(f"Campo vazio na posição A[{i+1},{j+1}]")
                    matriz[i, j] = float(valor)
                
                valor_b = self.vetor_entries[i].get().strip()
                if valor_b == "":
                    raise ValueError(f"Campo vazio na posição b[{i+1}]")
                vetor[i] = float(valor_b)
                
            return matriz, vetor, n
            
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"❌ {str(e)}\n\nPor favor, digite números válidos em todos os campos.")
            return None, None, None
    
    def gauss_jordan(self, matrix, vector):
        n = len(matrix)
        augmented = np.hstack([matrix, vector.reshape(-1, 1)])
        
        resultado = "🔧 RESOLUÇÃO PASSO A PASSO:\n" + "═" * 60 + "\n\n"
        resultado += "📐 Matriz aumentada inicial:\n"
        resultado += self.formatar_matriz(augmented) + "\n"
        
        # Eliminação
        for i in range(n):
            # Pivoteamento parcial
            max_row = i
            for k in range(i + 1, n):
                if abs(augmented[k, i]) > abs(augmented[max_row, i]):
                    max_row = k
            
            if max_row != i:
                augmented[[i, max_row]] = augmented[[max_row, i]]
                resultado += f"🔄 Troca linha {i+1} com linha {max_row+1}:\n"
                resultado += self.formatar_matriz(augmented) + "\n"
            
            if abs(augmented[i, i]) < 1e-10:
                raise ValueError("Sistema singular ou sem solução única")
            
            # Normaliza a linha do pivô
            pivot = augmented[i, i]
            augmented[i] = augmented[i] / pivot
            resultado += f"➗ Divide linha {i+1} por {pivot:.4f}:\n"
            resultado += self.formatar_matriz(augmented) + "\n"
            
            # Elimina outras linhas
            for j in range(n):
                if j != i:
                    factor = augmented[j, i]
                    augmented[j] = augmented[j] - factor * augmented[i]
                    resultado += f"✂️  Subtrai {factor:.4f}×L{i+1} de L{j+1}:\n"
                    resultado += self.formatar_matriz(augmented) + "\n"
        
        solution = augmented[:, -1]
        return solution, resultado
    
    def formatar_matriz(self, matriz):
        """Formata matriz para exibição bonita"""
        n_linhas, n_colunas = matriz.shape
        resultado = ""
        
        for i in range(n_linhas):
            linha = "│"
            for j in range(n_colunas):
                if j == n_linhas:  # Linha vertical para separar matriz aumentada
                    linha += " │ "
                valor = matriz[i, j]
                if abs(valor) < 1e-10:  # Tratar zeros
                    linha += f"{0:>10.4f}"
                else:
                    linha += f"{valor:>10.4f}"
            linha += " │"
            resultado += linha + "\n"
        
        return resultado
    
    def mostrar_sistema_formatado(self, matrix, vector, n):
        """Mostra o sistema de forma organizada e bonita"""
        resultado = "SISTEMA LINEAR DIGITADO:\n" + "═" * 50 + "\n\n"
        
        for i in range(n):
            equation = f"Eq {i+1}: "
            for j in range(n):
                coef = matrix[i, j]
                if j == 0:
                    if coef < 0:
                        equation += f"- {abs(coef):.2f}·x{j+1}"
                    else:
                        equation += f" {coef:.2f}·x{j+1}"
                else:
                    if coef >= 0:
                        equation += f" + {coef:.2f}·x{j+1}"
                    else:
                        equation += f" - {abs(coef):.2f}·x{j+1}"
            equation += f" = {vector[i]:.2f}"
            resultado += equation + "\n"
        
        resultado += "\n" + "═" * 50 + "\n\n"
        return resultado
    
    def formatar_solucao(self, solucao, n):
        """Formata a solução de forma bonita"""
        resultado = "SOLUÇÃO ENCONTRADA:\n" + "─" * 40 + "\n\n"
        
        for i in range(n):
            resultado += f"    x{i+1} = {solucao[i]:.6f}\n"
        
        resultado += "\n"
        return resultado
    
    def verificar_solucao(self, matriz, vetor, solucao, n):
        """Verifica a solução e formata os resultados"""
        resultado = "VERIFICAÇÃO:\n" + "─" * 40 + "\n\n"
        
        for i in range(n):
            calculado = sum(matriz[i, j] * solucao[j] for j in range(n))
            diferenca = abs(calculado - vetor[i])
            status = "✓" if diferenca < 1e-8 else "✗"
            resultado += f"Eq {i+1}: {calculado:.8f} ≈ {vetor[i]:.8f} {status}\n"
        
        resultado += "\n"
        return resultado
    
    def resolver_sistema(self):
        matriz, vetor, n = self.obter_sistema()
        
        if matriz is None:
            return
        
        try:
            # Limpar área de resultados
            self.text_resultados.delete(1.0, tk.END)
            
            # Mostrar sistema digitado
            sistema_str = self.mostrar_sistema_formatado(matriz, vetor, n)
            self.text_resultados.insert(tk.END, sistema_str)
            
            # Resolver sistema
            solucao, passos = self.gauss_jordan(matriz, vetor)
            
            # Mostrar resolução se solicitado
            if self.mostrar_resolucao.get():
                self.text_resultados.insert(tk.END, passos)
                self.text_resultados.insert(tk.END, "═" * 60 + "\n\n")

            # Mostrar verificação
            verificacao_str = self.verificar_solucao(matriz, vetor, solucao, n)
            self.text_resultados.insert(tk.END, verificacao_str)
            
            # Mostrar solução formatada
            solucao_str = self.formatar_solucao(solucao, n)
            self.text_resultados.insert(tk.END, solucao_str)
            
            
            # Adicionar mensagem de sucesso
            self.text_resultados.insert(tk.END, "Sistema resolvido com sucesso!\n")
                
        except ValueError as e:
            messagebox.showerror("Erro na Resolução", f"{str(e)}")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado:\n{str(e)}")
    
    def exemplo_2x2(self):
        """Carrega exemplo 2x2"""
        self.tamanho.set(2)
        self.gerar_campos()
        
        exemplo_matriz = [
            [2, 1],
            [1, -1]
        ]
        exemplo_vetor = [5, 1]
        
        self.preencher_campos(exemplo_matriz, exemplo_vetor)
    
    def exemplo_3x3(self):
        """Carrega exemplo 3x3"""
        self.tamanho.set(3)
        self.gerar_campos()
        
        exemplo_matriz = [
            [2, 1, -1],
            [-3, -1, 2],
            [-2, 1, 2]
        ]
        exemplo_vetor = [8, -11, -3]
        
        self.preencher_campos(exemplo_matriz, exemplo_vetor)
    
    def exemplo_4x4(self):
        """Carrega exemplo 4x4"""
        self.tamanho.set(4)
        self.gerar_campos()
        
        exemplo_matriz = [
            [2, 1, 0, 1],
            [1, -1, 2, 0],
            [0, 1, -1, 1],
            [1, 0, 1, -1]
        ]
        exemplo_vetor = [5, 1, 0, 2]
        
        self.preencher_campos(exemplo_matriz, exemplo_vetor)
    
    def preencher_campos(self, matriz, vetor):
        """Preenche os campos com os valores fornecidos"""
        n = len(matriz)
        
        for i in range(n):
            for j in range(n):
                self.matriz_entries[i][j].delete(0, tk.END)
                self.matriz_entries[i][j].insert(0, str(matriz[i][j]))
            
            self.vetor_entries[i].delete(0, tk.END)
            self.vetor_entries[i].insert(0, str(vetor[i]))
    
    def limpar_tudo(self):
        """Limpa todos os campos e resultados"""
        for linha in self.matriz_entries:
            for entry in linha:
                entry.delete(0, tk.END)
        
        for entry in self.vetor_entries:
            entry.delete(0, tk.END)
        
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, "💡 Digite os coeficientes e clique em 'Resolver Sistema'...\n")
    
    def copiar_resultados(self):
        """Copia os resultados para a área de transferência"""
        resultados = self.text_resultados.get(1.0, tk.END)
        if resultados.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(resultados)
            messagebox.showinfo("Copiado", "📋 Resultados copiados para a área de transferência!")

def main():
    root = tk.Tk()
    
    # Tentar usar tema mais moderno se disponível
    try:
        import ttkthemes
        style = ttkthemes.ThemedStyle(root)
        style.set_theme("arc")
    except:
        pass
    
    app = SistemaLinearApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
