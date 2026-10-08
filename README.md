# vesper — o username existe nesses perfis públicos?

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)

Confere se um username existe em perfis **públicos** de plataformas de código: GitHub, GitLab, Codeberg, Hugging Face, npm e dev.to. O apelido só entra no caminho de URLs fixas dessas plataformas. Nada de e-mail, telefone, endereço, documento ou base vazada.

Não é busca de pessoas. Use no seu próprio username, ou com consentimento.

## Por que “inconclusivo” não é “não existe”

| Resposta | Significa |
|---|---|
| `existe` | A API pública devolveu o perfil (ou, no GitLab, uma lista não vazia). |
| `não achei` | 404, ou lista vazia no GitLab. |
| `inconclusivo` | Timeout, bloqueio, cota ou status que não é 200 nem 404. Não trate como ausência. |

As consultas saem em paralelo (`ThreadPoolExecutor`, um worker por site), com timeout de 6 segundos. O corpo da resposta não é impresso — só site, estado, tempo e a URL do perfil.

## Stack

- **Python 3.11+**, só biblioteca padrão (`urllib.request`, sem `requests`)
- User-Agent fixo: `vesper/0.1 (+https://github.com/gabrielteramae/vesper)`
- CLI `vesper` ou `python -m vesper.cli`
- Username limitado a letras, números, ponto, `_` ou hífen, no máximo 39 caracteres

## Estrutura

```
vesper/
├── __init__.py
├── __main__.py
├── cli.py          # imprime existe / não achei / inconclusivo
├── check.py        # dispara as consultas em paralelo
└── sites.py        # URLs fixas e leitura do status (GitHub, GitLab, …)
tests/
└── test_sites.py   # username inválido, corpo do GitLab, hosts permitidos
```

## Como rodar

```bash
git clone https://github.com/gabrielteramae/vesper.git
cd vesper
python -m unittest discover -s tests -t .
python -m vesper.cli seu-username
```

Username inválido (espaço, `../`, esquema) sai com código 2 e a mensagem no stderr. Cada linha do relatório:

```
  GitHub           existe            120 ms  https://github.com/seu-username
  npm              não achei          80 ms  https://www.npmjs.com/~seu-username
  dev.to           inconclusivo      6000 ms https://dev.to/seu-username
```

## Sites consultados

| Site | Probe | Leitura |
|---|---|---|
| GitHub | `api.github.com/users/{u}` | 200 existe, 404 não achei |
| GitLab | `gitlab.com/api/v4/users?username={u}` | lista vazia = não achei |
| Codeberg | `codeberg.org/api/v1/users/{u}` | 200 / 404 |
| Hugging Face | `huggingface.co/api/users/{u}/overview` | 200 / 404 |
| npm | `registry.npmjs.org/-/user/org.couchdb.user:{u}` | 200 / 404 |
| dev.to | `dev.to/api/users/by_username?url={u}` | 200 / 404 |

A API do GitHub sem token tem cota baixa. Resposta inconclusiva não vira “não existe”.

## Testes realizados

`tests/test_sites.py` não chama a rede. Cobre normalização (`" Gabriel "` → `Gabriel`), rejeição de `../etc`, espaço e `javascript:`, o parser do GitLab (`[]` = missing, lista com item = found, 500 = unknown) e o fato de todo probe ficar em um host conhecido (`api.github.com`, `gitlab.com`, `codeberg.org`, `huggingface.co`, `registry.npmjs.org`, `dev.to`).

---

© 2026 Gabriel Teramae Chan
