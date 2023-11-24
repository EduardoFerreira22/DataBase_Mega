# import uuid

# def criar_uuid(dado):
#     # Converte o dado em um UUID
#     uuid_resultado = uuid.uuid5(uuid.NAMESPACE_DNS, dado)
#     return str(uuid_resultado).upper()

# # Exemplo de uso
# dado = "CRXPA-22805-VP4KN-OCNSK"
# uuid_gerado = criar_uuid(dado)
# print(uuid_gerado)


from cryptography.fernet import Fernet

# Função para gerar chave de criptografia
def gerar_chave():
    chave = Fernet.generate_key()
    return chave

# Função para criptografar um dado sensível
def criptografar_dado(chave, dado):
    fernet = Fernet(chave)
    dado_criptografado = fernet.encrypt(dado.encode())
    return dado_criptografado

# Função para descriptografar um dado sensível
def descriptografar_dado(chave, dado_criptografado):
    fernet = Fernet(chave)
    dado_descriptografado = fernet.decrypt(dado_criptografado).decode()
    return dado_descriptografado

# Exemplo de uso
chave = gerar_chave()
email_original = "usuario@example.com"

email_criptografado = criptografar_dado(chave, email_original)
print("Email Criptografado:", email_criptografado)

email_descriptografado = descriptografar_dado(chave, email_criptografado)
print("Email Descriptografado:", email_descriptografado)
