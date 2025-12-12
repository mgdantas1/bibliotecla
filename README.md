# Bibliotecla

<div align='center'>
    <img
        src='static/imagens/logo/logo.svg'
        loading='lazy'
        width='200'
        style='margin-top: 3rem'
        alt='Logo'
    >
</div>

## Como executar?

1. Certifique-se de criar uma database com o nome `db_bibliotecla` 

2. Verifique se as configurações estão corretas para o seu caso, se não, será preciso modificá-las dentro de `database/__init__.py`

    Configurações padrão:
    </br>
    **Porta: `3306`**
    </br>
    **Usuário: `root`**
    </br>
    **Conexão: `localhost`**

### No terminal:

**1. Clone o repositório**

```
    https://github.com/mgdantas1/bibliotecla.git
```

**2. Crie um ambiente virtual e o ative**

```
    # Criar...
    py -m venv env

    # Ativar...
    .\env\Scripts\activate
```

**3. Instale as pendências**

```
    pip install -r requirements.txt
```

**4. Rode a aplicação**

```
    py app.py
```

### No navegador digite `localhost:5000`
