
from datetime import datetime
import os
import shutil
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageFilter, ImageOps, ImageTk

def limpar_fotos():
    diretorio_fotos = os.getcwd()  # Obtém o diretório atual onde o programa está sendo executado
    extensoes_imagem = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')  # Extensões de imagem comuns

    # Verifica se o diretório existe
    if os.path.exists(diretorio_fotos) and os.path.isdir(diretorio_fotos):
        # Remove apenas arquivos de imagem do diretório
        for filename in os.listdir(diretorio_fotos):
            file_path = os.path.join(diretorio_fotos, filename)
            if filename.lower().endswith(extensoes_imagem):
                try:
                    os.unlink(file_path)
                    print(f'{filename} foi deletado com sucesso.')
                except Exception as e:
                    print(f'Erro ao deletar {file_path}. Razão: {e}')
        print('Todas as imagens foram removidas com sucesso!')
    else:
        print('Diretório não encontrado.')

# Classes de Manipulação de Imagem e Filtros
class Imagem:
    def __init__(self, caminho):
        self.caminho = caminho
        self.imagem = self.carregar_imagem()

    def carregar_imagem(self):
        if os.path.exists(self.caminho):
            try:
                return Image.open(self.caminho)
            except Exception as e:
                messagebox.showerror("Erro ao carregar imagem", f"Erro ao carregar imagem: {e}")
                return None
        else:
            messagebox.showerror("Arquivo não encontrado", f"Arquivo não encontrado: {self.caminho}")
            return None

    def salvar_imagem(self, caminho):
      if self.imagem:
          try:
            # Gera um nome de arquivo único com timestamp
              timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
              nome_base, extensao = os.path.splitext(caminho)
              novo_caminho = f"{nome_base}_{timestamp}{extensao}"
            
              self.imagem.save(novo_caminho)
              print(f"Imagem salva com sucesso em {novo_caminho}")                
          except Exception as e:
              print(f"Erro ao salvar imagem: {e}")
      else:
          print("Nenhuma imagem carregada para salvar.")
          
    def aplicar_filtro(self, filtro):
        if self.imagem:
            self.imagem = filtro.aplicar(self.imagem)
        else:
            print("Nenhuma imagem carregada para aplicar o filtro.")

class DialogoEscolhaImagem:
    def __init__(self, parent, callback, x=100, y=100):
        self.top = tk.Toplevel(parent)
        self.top.title("Escolha Imagem")
        self.top.geometry("500x200+{}+{}".format(x, y))
        self.top.configure(bg="lightblue")  # Altere a cor para o que desejar

        self.callback = callback

        # Texto de instrução
        self.instrucoes = tk.Label(self.top, text="Você quer adicionar uma imagem local ou baixar uma da internet?", font=("Helvetica", 12, "bold"),bg="lightblue")
        self.instrucoes.pack(pady=10)

        # Botão para imagem local
        self.btn_local = tk.Button(self.top, text="Adicionar Imagem Local", command=self.adicionar_local, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
        self.btn_local.pack(pady=10)

        # Botão para baixar da internet
        self.btn_internet = tk.Button(self.top, text="Baixar Imagem da Internet", command=self.baixar_internet, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
        self.btn_internet.pack(pady=5)

        # Botão para cancelar
        self.btn_cancelar = tk.Button(self.top, text="Cancelar", command=self.cancelar, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
        self.btn_cancelar.pack(pady=10)

    def adicionar_local(self):
        self.callback('local')
        self.top.destroy()

    def baixar_internet(self):
        self.callback('internet')
        self.top.destroy()

    def cancelar(self):
        self.callback('cancelar')
        self.top.destroy()

class FilterMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message, ok_callback=None, cancel_callback=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x150")
        self.parent = parent

        # Configuração da cor de fundo
        self.configure(bg="lightblue")

        # Texto da mensagem
        self.message_label = tk.Label(self, text=message, font=("Helvetica", 12, "bold"), bg="lightblue", fg="black", padx=20, pady=20)
        self.message_label.pack()

        # Frame para os botões
        self.button_frame = tk.Frame(self, bg="lightblue")
        self.button_frame.pack(pady=10)

        # Botão OK
        self.ok_button = tk.Button(self.button_frame, text="OK", command=self.ok, bg="lightgray", fg="black", font=("Helvetica", 12, "bold"))
        self.ok_button.pack(side=tk.LEFT, padx=10)

        # Botão Cancelar (se fornecido)
        if cancel_callback:
            self.cancel_button = tk.Button(self.button_frame, text="Cancelar", command=self.cancel, bg="lightgray", fg="black", font=("Helvetica", 12, "bold"))
            self.cancel_button.pack(side=tk.LEFT, padx=10)
            self.cancel_callback = cancel_callback
        else:
            self.cancel_button = None

        self.ok_callback = ok_callback

    def ok(self):
        if self.ok_callback:
            self.ok_callback()
        self.destroy()

    def cancel(self):
        if self.cancel_callback:
            self.cancel_callback()
        self.destroy()

def show_Filter_messagebox(parent, title, message, ok_callback=None, cancel_callback=None):
    box = FilterMessageBox(parent, title, message, ok_callback, cancel_callback)
    parent.wait_window(box)

class Download:
    @staticmethod
    def baixar_imagem(url, destino):
        try:
            resposta = requests.get(url, allow_redirects=True)
            resposta.raise_for_status()
            with open(destino, 'wb') as arquivo:
                arquivo.write(resposta.content)
            print(f"Imagem baixada e salva em {destino}")
        except Exception as e:
            print(f"Erro ao baixar imagem: {e}")

# Filtros
class FiltroEscalaCinza:
    @staticmethod
    def aplicar(imagem):
        return ImageOps.grayscale(imagem)

class FiltroPretoBranco:
    @staticmethod
    def aplicar(imagem):
        return imagem.convert("1")

class FiltroCartoon:
    @staticmethod
    def aplicar(imagem):
        return imagem.filter(ImageFilter.EDGE_ENHANCE)

class FiltroNegativo:
    @staticmethod
    def aplicar(imagem):
        return ImageOps.invert(imagem)

class FiltroContorno:
    @staticmethod
    def aplicar(imagem):
        return imagem.filter(ImageFilter.CONTOUR)

class FiltroBlurred:
    @staticmethod
    def aplicar(imagem):
        return imagem.filter(ImageFilter.BLUR)

# Classe da Interface Gráfica
class AplicacaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imagens")
        self.root.geometry("1920x1080")
        self.imagem = None

        # Adicionando uma imagem de fundo
        self.bg_image = Image.open("C:/Users/Vinicius/Desktop/imagem.jpg")
        self.bg_image = self.bg_image.resize((1920, 1080),Image.Resampling.LANCZOS)  # Redimensiona a imagem para caber na janela
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche toda a janela com a imagem


        # Botões da Interface
        self.btn_adicionar_imagem = tk.Button(root, text="Adicionar Imagem", command=self.adicionar_imagem,
                                      bg="lightblue", fg="black", font=("Helvetica", 12, "bold"), width=20)
        self.btn_adicionar_imagem.pack(pady=10)
        self.btn_adicionar_imagem.place(x=50, y=50, width=150, height=60)


        


        self.btn_aplicar_filtro = tk.Button(root, text="Escolher Filtro", command=self.escolher_filtro,
                                      bg="lightblue", fg="black", font=("Helvetica", 12, "bold"), width=20)
        self.btn_aplicar_filtro.pack(pady=10)
        self.btn_aplicar_filtro.place(x=50, y=150, width=150, height=60)

        self.btn_mostrar_imagens = tk.Button(root, text="Mostrar Imagens", command=self.mostrar_imagens,
                                      bg="lightblue", fg="black", font=("Helvetica", 12, "bold"), width=20)
        self.btn_mostrar_imagens.pack(pady=10)
        self.btn_mostrar_imagens.place(x=50, y=250, width=150, height=60)

        self.btn_sair = tk.Button(root, text="Sair", command=root.quit,
                                      bg="lightblue", fg="black", font=("Helvetica", 12, "bold"), width=20)
        
        self.btn_limpar_fotos = tk.Button(root, text="Limpar Fotos", bg="lightblue", fg="black",
                             font=("Helvetica", 12, "bold"), width=20, height=2, command=limpar_fotos)
        self.btn_limpar_fotos.place(x=50, y=350, width=150, height=60)

        self.btn_sair.pack(pady=10)
        self.btn_sair.place(x=50, y=700, width=150, height=30)

        self.lbl_imagem = tk.Label(root)
        self.lbl_imagem.pack(pady=10)

    def adicionar_imagem(self):
        x_pos = 600
        y_pos = 250
        DialogoEscolhaImagem(self.root, self.processar_escolha_imagem, x=x_pos, y=y_pos)


    def processar_escolha_imagem(self, escolha):
        if escolha == 'local':
            caminho = filedialog.askopenfilename(title="Escolha a Imagem", filetypes=[("Image Files", "*.jpg *.png")])
            if caminho:
                self.imagem = Imagem(caminho)
                self.exibir_imagem(self.imagem.imagem)
        elif escolha == 'internet':
            url = tk.simpledialog.askstring("URL da Imagem", "Digite a URL da imagem:")
            if url:
                destino = "imagem_baixada.jpg"
                Download.baixar_imagem(url, destino)
                self.imagem = Imagem(destino)
                self.exibir_imagem(self.imagem.imagem)
        elif escolha == 'cancelar':
            # Ação de cancelamento, se necessário
            pass

    def escolher_filtro(self):
        if not self.imagem:
            show_Filter_messagebox(self.root, "Nenhuma Imagem", "Por favor, adicione uma imagem primeiro.")
            return

        # Cria a janela de escolha de filtro
        filtro_window = tk.Toplevel(self.root)
        filtro_window.title("Escolha o Filtro")
        filtro_window.geometry("300x300+{}+{}".format(self.root.winfo_screenwidth() // 2 - 150, self.root.winfo_screenheight() // 2 - 150))
        filtro_window.configure(bg="lightblue")

        filtros = {
            'FiltroEscalaCinza': FiltroEscalaCinza(),
            'FiltroPretoBranco': FiltroPretoBranco(),
            'FiltroCartoon': FiltroCartoon(),
            'FiltroNegativo': FiltroNegativo(),
            'FiltroContorno': FiltroContorno(),
            'FiltroBlurred': FiltroBlurred()
        }

        tk.Label(filtro_window, text="Escolha um filtro:", font=("Helvetica", 12, "bold"), bg="lightblue").pack(pady=10)

        def aplicar_filtro(escolha):
            if escolha in filtros:
                self.imagem.aplicar_filtro(filtros[escolha])
                self.imagem.salvar_imagem(f"imagem_filtrada_{escolha}.jpg")
                self.exibir_imagem(self.imagem.imagem)
                messagebox.showinfo("Sucesso", "Filtro aplicado e imagem salva.")
            else:
                messagebox.showerror("Erro", "Filtro inválido.")
            filtro_window.destroy()

        for chave, filtro in filtros.items():
            tk.Button(filtro_window, text=f"Filtro {chave}", command=lambda chave=chave: aplicar_filtro(chave),
                      bg="lightgray", fg="black", font=("Helvetica", 12, "bold")).pack(pady=5, fill=tk.X, padx=10)

    def mostrar_imagens(self):
      arquivos = [f for f in os.listdir() if f.endswith(('.jpg', '.png'))]
      if arquivos:      
          img_window = tk.Toplevel(self.root)
          img_window.title("Imagens no Diretório")
          img_window.config(bg='lightblue')


        # Configuração do tamanho e espaçamento das imagens
          tamanho_imagem = (200, 200)
          espaco_horizontal = 20
          espaco_vertical = 20

        # Número máximo de imagens por linha
          max_por_linha = 4

        # Calcula o número de linhas necessárias
          num_imagens = len(arquivos)
          num_linhas = (num_imagens + max_por_linha - 1) // max_por_linha

        # Cria o grid
          for i, arquivo in enumerate(arquivos):
              img = Image.open(arquivo)
              img.thumbnail(tamanho_imagem)  # Redimensiona a imagem
              img_tk = ImageTk.PhotoImage(img)

            # Calcula a posição (linha e coluna) no grid
              linha = i // max_por_linha
              coluna = i % max_por_linha

              lbl_img = tk.Label(img_window, image=img_tk)
              lbl_img.image = img_tk  # Necessário para evitar que o garbage collector remova a imagem

            # Adiciona o label ao grid
              lbl_img.grid(row=linha, column=coluna, padx=espaco_horizontal, pady=espaco_vertical)

        # Ajusta a janela para caber no conteúdo
          img_window.update_idletasks()
          img_window.geometry(f'{max_por_linha * (tamanho_imagem[0] + espaco_horizontal)}x{num_linhas * (tamanho_imagem[1] + espaco_vertical)}')
      else:
          show_Filter_messagebox(self.root, "Nenhuma Imagem", "Não há imagens no diretório.")


    def exibir_imagem(self, imagem, tamanho=(800, 600), pos_x=550, pos_y=100):
      if imagem:
        # Redimensiona a imagem para o tamanho especificado
        imagem_redimensionada = imagem.resize(tamanho, Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(imagem_redimensionada)
        
        
        # Atualiza a Label com a imagem redimensionada
        self.lbl_imagem.config(image=img_tk)
        self.lbl_imagem.image = img_tk  # Necessário para evitar que o garbage collector remova a imagem

        # Posiciona a Label com a imagem
        self.lbl_imagem.place(x=pos_x, y=pos_y, width=tamanho[0], height=tamanho[1])




if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoGUI(root)
    root.mainloop()
