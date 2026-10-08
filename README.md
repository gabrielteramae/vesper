# vesper

Confere se um username existe em perfis **públicos** de plataformas de código: GitHub, GitLab, Codeberg, Hugging Face, npm e dev.to.

Não é busca de pessoas. Não olha e-mail, telefone, endereço, documento ou base vazada. O apelido só entra no caminho de URLs fixas dessas plataformas. Use no seu próprio username, ou com consentimento.

## Rodar

```bash
python -m unittest discover -s tests -t .
python -m vesper.cli seu-username
```

Cada linha sai como `existe`, `não achei` ou `inconclusivo` (limite de API, bloqueio ou rede). Nada do corpo da resposta é impresso.

## Limites

São poucas consultas em paralelo, com timeout curto. As APIs públicas têm cota — em especial a do GitHub sem token. Se a resposta for inconclusiva, não trate como “não existe”.
