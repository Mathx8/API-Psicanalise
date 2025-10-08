## 🧠 Clínica de Psicologia - API RESTful

Esta API proporciona os principais recursos para o gerenciamento interno de uma clínica de psicologia, tais como cadastro de pacientes, psicólogos, salas, sessões de terapia, laudos e disponibilidades. Toda a documentação é automaticamente gerada pelo Swagger, via Flask-RESTX.

*diagrama aqui*

### 🛠 Tecnologias utilizadas

- **Python**
- **Flask**
- **SQLAlchemy**
- **SQLite**
- **Swagger UI**
- **Docker**
- **Estrutura MVC**

***

## ▶️ Instalação

1. Clone o projeto:

```
git clone <seu-repositório>
cd <pasta-do-projeto>
```

2. Crie e ative um ambiente virtual:

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instale as dependências:

```
pip install -r requirements.txt
```

4. Execute a aplicação:

```
python app.py
```

5. Acesse a documentação interativa do Swagger em:
http://localhost:5000/

***

## 🔄 Endpoints

### Pacientes

- **GET /paciente/** – Lista de todos os pacientes.
- **POST /paciente/** – Cadastro de paciente.
- **GET /paciente/{id}** – Consulta por ID.
- **PUT /paciente/{id}** – Atualiza cadastro do paciente.
- **DELETE /paciente/{id}** – Exclui um paciente.

**Modelo de entrada**:

```json
{
  "nome": "Tiago",
  "idade": 20,
  "genero": "Masculino",
  "telefone": "1140028922",
  "email": "tiago@gmail.com",
  "senha": "******"
}
```


***

### Psicólogos

- **GET /psicologo/** – Lista de todos os psicólogos.
- **POST /psicologo/** – Cadastro de psicólogo.
- **GET /psicologo/{id}** – Consulta por ID.
- **PUT /psicologo/{id}** – Atualiza cadastro do psicólogo.
- **DELETE /psicologo/{id}** – Deleta psicólogo.

**Modelo de entrada**:

```json
{
  "crp": "12345-SP",
  "nome": "Tiago",
  "idade": 20,
  "telefone": "1140028922",
  "especializacao": "Psicologia Clínica",
  "email": "tiago@gmail.com",
  "senha": "******"
}
```


***

### Salas

- **GET /sala/** – Lista todas as salas.
- **POST /sala/** – Cadastro de sala.
- **GET /sala/{id}** – Consulta por ID.
- **PUT /sala/{id}** – Atualiza sala.
- **DELETE /sala/{id}** – Exclui sala.

**Modelo de entrada**:

```json
{
  "nome": "A1",
  "descricao": "Sala de atendimento principal"
}
```


***

### Disponibilidades

- **GET /disponibilidade/** – Lista todas as disponibilidades.
- **POST /disponibilidade/** – Cadastra uma nova disponibilidade.
- **GET /disponibilidade/{id}** – Consulta por ID.
- **PUT /disponibilidade/{id}** – Atualiza disponibilidade existente.
- **DELETE /disponibilidade/{id}** – Exclui.
- **GET /disponibilidade/dia/{data}** – Lista por dia.
- **GET /disponibilidade/semana/{inicio}/{fim}** – Lista por semana.

**Modelo de entrada**:

```json
{
  "id_psicologo": 1,
  "id_sala": 2,
  "data": "2025-10-10",
  "horario_inicial": "09:00",
  "horario_final": "12:00"
}
```


***

### Terapias

- **GET /terapia/** – Lista todas as sessões de terapia.
- **POST /terapia/** – Cadastra sessão.
- **GET /terapia/{id}** – Consulta por ID.
- **PUT /terapia/{id}** – Atualiza sessão.
- **DELETE /terapia/{id}** – Exclui.
- **GET /terapia/dia/{data}/[psicologo_id]** – Lista sessões por dia (com filtro opcional).
- **GET /terapia/semana/{inicio}/{fim}/[psicologo_id]** – Lista por semana (com filtro opcional).

**Modelo de entrada**:

```json
{
  "id_psicologo": 1,
  "id_paciente": 23,
  "id_sala": 2,
  "data": "2025-10-10 10:30",
  "duracao": "01:00",
  "numero_sessao": 1
}
```


***

### Laudos

- **GET /laudo/** – Lista todos os laudos.
- **POST /laudo/** – Cadastra laudo.
- **GET /laudo/{id}** – Consulta por ID.
- **PUT /laudo/{id}** – Atualiza laudo existente.
- **DELETE /laudo/{id}** – Exclui.

**Modelo de entrada**:

```json
{
  "id_terapia": 1,
  "texto": "Paciente apresentou evolução positiva durante a sessão."
}
```
***

## 📁 Organização do Projeto (Arquitetura MVC)

```
.
├── Controller/
|   └── router_disponibilidade.py
|   └── router_laudo.py
|   └── router_paciente.py
|   └── router_psicologo.py
|   └── router_sala.py
|   └── router_terapia.py
├── Docker/
│       └── Dockerfile
│       └── docker-compose.yml
├── Model/
|   └── disponibilidade_model.py
|   └── laudo_model.py
|   └── paciente_model.py
|   └── psicologo_model.py
|   └── sala_model.py
|   └── terapia_model.py
├── Swagger/
│       └── namespace/
|           └── disponibilidade_namespace.py
|           └── laudo_namespace.py
|           └── paciente_namespace.py
|           └── paciente_namespace.py
|           └── sala_namespace.py
|           └── terapia_namespace.py
|       └── __init__.py
|       └── swagger_config.py
├── .gitignore
├── README.md
├── app.py
├── config.py
├── database.py
├── psicanalise.db
└── requirements.txt
```

***

## 💻 Equipe de Desenvolvimento

[Matheus de Queiroz Mendanha]

[Tiago Genari Caldeira]

[Matheus de Queiroz Mendanha]: https://github.com/Mathx8

[Tiago Genari Caldeira]: https://github.com/genari05