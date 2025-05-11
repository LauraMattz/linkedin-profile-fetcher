# LinkedIn Profile Fetcher 🚀

Este projeto permite buscar e exibir informações de perfis do LinkedIn usando a API ProxyCurl, com suporte a cache local e uma interface de terminal rica e interativa. 🎉

## Funcionalidades ✨
- Busca de dados de perfis do LinkedIn via API ProxyCurl.
- Cache local para evitar requisições desnecessárias.
- Exibição estilizada no terminal usando a biblioteca `rich`.

## Pré-requisitos 🛠️
- Python 3.8 ou superior.
- Uma conta na [ProxyCurl](https://nubela.co/proxycurl) para obter uma chave de API.

## Configuração ⚙️

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/linkedin-profile-fetcher.git
   cd linkedin-profile-fetcher
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure a chave de API como variável de ambiente:
   ```bash
   export PROXYCURL_API_KEY="sua-chave-aqui"  # No Windows: set PROXYCURL_API_KEY=sua-chave-aqui
   ```

4. Edite a lista de URLs do LinkedIn no arquivo `proxycurl.py`:
   ```python
   LINKEDIN_URLS = [
       "https://www.linkedin.com/in/exemplo/",
   ]
   ```

## Uso 🚀
Execute o script:
```bash
python proxycurl.py
```

## Exemplo de Saída 📋
![Exemplo de saída](https://via.placeholder.com/800x400?text=Exemplo+de+Sa%C3%ADda)

## Contribuição 🤝
Sinta-se à vontade para abrir issues ou enviar pull requests. Toda ajuda é bem-vinda! 💡

## Licença 📜
Este projeto está licenciado sob a [MIT License](LICENSE).
