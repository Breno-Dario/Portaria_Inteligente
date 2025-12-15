<h2>Portaria Inteligente – Reconhecimento Facial com Registro de Acessos</h2>

Sistema de controle de acesso utilizando reconhecimento facial, interface gráfica em Tkinter, e geração automática de logs de acesso.
Desenvolvido para fins acadêmicos por Breno Dario e Alexandre Jesus.

<h2>Funcionalidades</h2>

- Reconhecimento facial em tempo real (Eigenfaces, Fisherfaces e LBPH)
- Controle de acesso com temporizador (liberação válida por 30s)
- Registro de acessos em arquivo .txt
- Interface gráfica moderna utilizando Tkinter
- Módulo para visualização imediata dos registros
- Suporte para múltiplos usuários
- Tratamento de erros, logs e informações detalhadas
- Compatível com Windows, Linux e macOS

<h2>Estrutura do Projeto</h2>

```SHELL
📁 projeto/
│
├── dataset/
│   ├── Usuario1/
│   ├── Usuario2/
│   └── ...
│
├── face_names.pickle
├── eigen_classifier.yml
├── fisher_classifier.yml
├── lbph_classifier.yml
│
├── acessos_registrados.txt
├── treino_faces.py        (parte de treinamento)
├── portaria_inteligente.py (código principal)
└── README.md
```

 <h2>Requisitos</h2>

**Python 3.8+**

Instale as dependências:
```bash
pip install opencv-contrib-python
pip install numpy
pip install Pillow
pip install tk

```

Certifique-se de que possui o OpenCV com módulos contrib, pois o recognizer LBPH, Eigen e Fisher estão nele.

<h2>Dataset – Como organizar</h2>

Cada usuário deve ter sua pasta com fotos:

```bash
dataset/
   Breno_Dario_RA1371392322016/
       1.jpg
       2.jpg
       ...
   Alexandro_Jesus_RA1371392322041.1/
       1.jpg
       2.jpg
```

Os nomes das pastas devem seguir o padrão:

```nginx
Nome_Sobrenome_RA123456789
```

<h2>Treinamento do Reconhecedor</h2>

O bloco inicial do seu código:

```python
ids, faces, face_names = get_image_data(training_path)
eigen_classifier.train(faces, ids)
fisher_classifier.train(faces, ids)
lbph_classifier.train(faces, ids)
```

Executa:

- Extração das imagens

- Conversão para escala de cinza

- Redimensionamento

- Geração dos reconhecedores:

   - `eigen_classifier.yml`

   - `fisher_classifier.yml`

   - `lbph_classifier.yml`

- Gera também `face_names.pickle`

**Para treinar novamente, basta rodar:**

```bash
python treino_faces.py
```

<h2>Execução do Sistema de Portaria</h2>

Para iniciar o sistema com interface Tkinter:

```bash
python portaria_inteligente.py
```

A aplicação inicia com:

-  Webcam ao vivo

- Nome e RA reconhecidos

- Tempo de acesso liberado

- Último registro salvo

- Botão para abrir o arquivo de logs

- Controle de Acesso

<h2>O sistema utiliza:</h2>

```python
authorized_people = {
    "Breno_Dario_RA1371392322016", 
    "Alexandro_Jesus_RA1371392322041.1"
}
```

- Somente usuários presentes na lista têm acesso liberado
- Usuários desconhecidos têm acesso negado
- Acesso é liberado por 30 segundos
- Registros são salvos no arquivo:

```nginx
acessos_registrados.txt
```

<h2>Formato do log:</h2>

```bash
Data/Hora      Nome            RA            Status
---------------------------------------------------------
02/12/2025 15:01:25  Breno Dario    RA1371392322016   LIBERADO
02/12/2025 15:02:10  Desconhecido   N/A               NEGADO
```

<h2>Interface – Recursos</h2>

A UI possui:

**Botões**

- Iniciar Reconhecimento

- Parar

- Sair do Sistema

- Visualizar Registros


**Painéis**

- Status do sistema

- Nome do usuário reconhecido

- RA

- Tempo restante

- Último registro atualizado em tempo real

<h2>Tecnologias Utilizadas</h2>

- Python 3

- OpenCV (com contrib)

- Numpy

- Tkinter

- Pillow

- Haarcascade para detecção facial

<h2>Dicas de Melhor Uso</h2>

- Tenha fotos variadas na pasta de treinamento
- Use boa iluminação
-  Mantenha distância adequada da câmera
-  Quanto mais imagens por usuário, melhor a precisão

<h2>Autores</h2>

- Breno Dario
- Alexandre Jesus

Sistemas de Informação – 2025
Projeto: **Portaria Inteligente com Reconhecimento Facial**
