import sqlite3

# Caminho do seu banco SQLite
DB_PATH = "psicanalise.db"

def adicionar_paciente(nome, idade, genero, telefone, email, senha_bash):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Inserção
        cursor.execute("""
            INSERT INTO pacientes (nome, idade, genero, telefone, email, senha_bash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, idade, genero, telefone, email, senha_bash))

        conn.commit()
        print(f"Paciente '{nome}' inserido com sucesso!")

    except sqlite3.Error as erro:
        print("Erro ao inserir paciente:", erro)

    finally:
        conn.close()


if __name__ == "__main__":
    # Paciente solicitado
    adicionar_paciente(
        nome="Katherine Mauricio",
        idade=28,
        genero="Feminino",
        telefone="(00) 00000-0000",
        email="katherine@gmail.com",
        senha_bash="123456"
    )
