import csv, random, unicodedata
from datetime import date, datetime, timedelta

random.seed(42)
N_VEND, N_PROD = 2000, 2000

UFS = {
    "SP": ["São Paulo", "Campinas", "Santos", "Ribeirão Preto", "Sorocaba"],
    "RJ": ["Rio de Janeiro", "Niterói", "Petrópolis"],
    "MG": ["Belo Horizonte", "Uberlândia", "Juiz de Fora"],
    "DF": ["Brasília"],
    "GO": ["Goiânia", "Anápolis"],
    "PR": ["Curitiba", "Londrina", "Maringá"],
    "SC": ["Florianópolis", "Joinville", "Blumenau"],
    "RS": ["Porto Alegre", "Caxias do Sul"],
    "BA": ["Salvador", "Feira de Santana"],
    "PE": ["Recife", "Olinda"],
    "CE": ["Fortaleza"],
    "AM": ["Manaus"],
    "PA": ["Belém"],
}
UF_PESO = {"SP": 30, "RJ": 12, "MG": 12, "DF": 5, "GO": 4, "PR": 8, "SC": 6, "RS": 7,
           "BA": 5, "PE": 4, "CE": 3, "AM": 2, "PA": 2}
UF_NOME = {"SP": "São Paulo", "RJ": "Rio de Janeiro", "MG": "Minas Gerais", "DF": "Distrito Federal",
           "PR": "Paraná", "BA": "Bahia"}

# categoria -> (variações sujas, itens, faixa de preço)
CATS = {
    "Eletrônicos": (["eletronicos", "ELETRÔNICOS", "Eletronicos ", "Eletrônico"],
                    ["Fone Bluetooth", "Smartwatch", "Carregador Turbo", "Caixa de Som", "Mouse Sem Fio",
                     "Teclado Mecânico", "Webcam Full HD", "Power Bank"], (49, 1800)),
    "Casa e Cozinha": (["casa e cozinha", "Casa & Cozinha", "CASA E COZINHA", "Casa/Cozinha"],
                       ["Panela Antiaderente", "Jogo de Facas", "Liquidificador", "Air Fryer", "Garrafa Térmica",
                        "Tábua de Corte", "Cafeteira"], (25, 900)),
    "Moda": (["moda", "MODA", "Moda ", "Vestuário"],
             ["Camiseta Algodão", "Calça Jeans", "Tênis Casual", "Jaqueta Corta-Vento", "Boné", "Mochila"], (29, 450)),
    "Beleza": (["beleza", "BELEZA", "Beleza e Saúde", "Beleza "],
               ["Hidratante Facial", "Protetor Solar", "Secador de Cabelo", "Perfume", "Kit Maquiagem"], (19, 600)),
    "Esporte": (["esporte", "Esportes", "ESPORTE", "Esporte e Lazer"],
                ["Halter 5kg", "Tapete de Yoga", "Bola de Futebol", "Corda de Pular", "Bicicleta Aro 29"], (15, 2500)),
    "Livros": (["livros", "LIVROS", "Livro", "Livros "],
               ["Livro de Python", "Romance Nacional", "Livro Infantil", "Guia de SQL", "Box de Fantasia"], (20, 250)),
    "Pet": (["pet", "PET", "Pet Shop", "Pets"],
            ["Ração Premium 10kg", "Arranhador", "Cama para Cachorro", "Coleira", "Areia Sanitária"], (15, 400)),
}
CAT_NOMES = list(CATS)
MARCAS = ["Atlas", "Nova", "Prime", "Vértice", "Aurora", "Zenith", "Boreal", "Lumina", "Orion", "Pampa"]
VARIANTES = ["Preto", "Branco", "Azul", "Cinza", "Grande", "Pequeno", "Pro", "Max", "Lite", "2.0"]

PREF = ["Loja", "Mercado", "Empório", "Casa", "Ponto", "Central", "Mega", "Super", "Top", "Bazar"]
NUCL = ["do Sol", "Brasil", "Estrela", "Ipê", "Cerrado", "Litoral", "Serra", "Horizonte", "Paraíso", "União",
        "Aliança", "Progresso", "Vitória", "Esperança", "Primavera", "Atlântico", "Amazônia", "Pantanal"]
SUF = ["", " Store", " Shop", " Digital", " Online", " & Cia", " Express", " Outlet"]
JUR = ["LTDA", "ME", "EIRELI", "S.A."]


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def cnpj_valido():
    n = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
    for pesos in ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]):
        r = sum(a * b for a, b in zip(n, pesos)) % 11
        n.append(0 if r < 2 else 11 - r)
    return "".join(map(str, n))


def fmt_cnpj(c):
    r = random.random()
    if r < 0.55:
        return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"
    if r < 0.85:
        return c
    if r < 0.93:
        return f"{c[:2]}{c[2:5]}{c[5:8]}/{c[8:12]}-{c[12:]}"
    if r < 0.97:
        return c[:-1] + str((int(c[-1]) + 3) % 10)  # dígito verificador inválido
    return ""


def fmt_data(d, mix=True):
    if not mix:
        return d.strftime("%Y-%m-%d")
    r = random.random()
    if r < 0.6:
        return d.strftime("%Y-%m-%d")
    if r < 0.85:
        return d.strftime("%d/%m/%Y")
    if r < 0.95:
        return d.strftime("%Y/%m/%d")
    return d.strftime("%d-%m-%Y")


def fmt_tel(uf_ddd):
    num = f"9{random.randint(1000,9999)}{random.randint(1000,9999)}"
    r = random.random()
    if r < 0.4:
        return f"({uf_ddd}) {num[:5]}-{num[5:]}"
    if r < 0.7:
        return f"{uf_ddd}{num}"
    if r < 0.85:
        return f"+55 {uf_ddd} {num}"
    if r < 0.95:
        return f"{uf_ddd} {num[:5]} {num[5:]}"
    return ""


DDD = {"SP": "11", "RJ": "21", "MG": "31", "DF": "61", "GO": "62", "PR": "41", "SC": "48", "RS": "51",
       "BA": "71", "PE": "81", "CE": "85", "AM": "92", "PA": "91"}


def sujar_id(i, prefixo):
    r = random.random()
    if r < 0.88:
        return i
    if r < 0.93:
        return i.lower()
    if r < 0.97:
        return f" {i} "
    return i.replace("-", "")


def fmt_preco(v):
    r = random.random()
    if r < 0.55:
        return f"{v:.2f}"
    if r < 0.75:
        return f"{v:.2f}".replace(".", ",")
    if r < 0.88:
        s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {s}"
    if r < 0.93:
        return f"R${v:.2f}"
    if r < 0.96:
        return f"{-v:.2f}"  # negativo
    return ""


# ---------------- VENDEDORES ----------------
vendedores, nomes_usados = [], set()
ufs, pesos = list(UF_PESO), list(UF_PESO.values())
hoje = date(2026, 10, 31)
for k in range(1, N_VEND + 1):
    vid = f"VND-{k:05d}"
    while True:
        fantasia = f"{random.choice(PREF)} {random.choice(NUCL)}{random.choice(SUF)}"
        if fantasia not in nomes_usados or random.random() < 0.02:
            break
    nomes_usados.add(fantasia)
    uf = random.choices(ufs, pesos)[0]
    cidade = random.choice(UFS[uf])
    cat = random.choice(CAT_NOMES)
    cadastro = date(2019, 1, 1) + timedelta(days=random.randint(0, (date(2026, 6, 30) - date(2019, 1, 1)).days))
    atualizado = datetime.combine(cadastro, datetime.min.time()) + timedelta(
        days=random.randint(0, (hoje - cadastro).days), seconds=random.randint(0, 86399))
    status = random.choices(["ativo", "inativo", "suspenso"], [85, 11, 4])[0]
    vendedores.append(dict(id=vid, fantasia=fantasia, cnpj=cnpj_valido(), uf=uf, cidade=cidade, cat=cat,
                           cadastro=cadastro, atualizado=atualizado, status=status,
                           nota=round(random.triangular(1, 5, 4.4), 1)))

V_COLS = ["seller_id", "nome_fantasia", "razao_social", "cnpj", "email", "telefone", "cidade", "uf",
          "categoria_principal", "data_cadastro", "status", "avaliacao_media", "updated_at"]


def linha_vendedor(v, atualizado=None, status=None):
    fantasia = v["fantasia"]
    r = random.random()
    nome_out = fantasia if r < 0.8 else (fantasia.upper() if r < 0.88 else (f"  {fantasia} " if r < 0.95 else fantasia.lower()))
    razao = f"{sem_acento(fantasia).upper().replace(' & ', ' E ')} {random.choice(JUR)}"
    slug = sem_acento(fantasia).lower().replace(" ", "").replace("&", "e")
    email = f"contato@{slug}.com.br"
    r = random.random()
    if r < 0.04:
        email = email.replace("@", "")
    elif r < 0.07:
        email = ""
    elif r < 0.12:
        email = email.upper()
    cidade = v["cidade"]
    r = random.random()
    if r < 0.12:
        cidade = sem_acento(cidade)
    elif r < 0.2:
        cidade = cidade.upper()
    elif r < 0.24:
        cidade = f" {cidade.lower()}"
    elif r < 0.26:
        cidade = ""
    uf = v["uf"]
    r = random.random()
    if r < 0.1:
        uf = uf.lower()
    elif r < 0.14 and uf in UF_NOME:
        uf = UF_NOME[uf]
    elif r < 0.16:
        uf = ""
    cat_out = v["cat"] if random.random() < 0.7 else random.choice(CATS[v["cat"]][0])
    st = status or v["status"]
    r = random.random()
    st_out = st if r < 0.6 else (st.upper() if r < 0.75 else (st.capitalize() + " " if r < 0.9 else ("" if r < 0.95 else {"ativo": "A", "inativo": "I", "suspenso": "S"}[st])))
    nota = v["nota"]
    r = random.random()
    nota_out = f"{nota}" if r < 0.75 else (f"{nota}".replace(".", ",") if r < 0.88 else ("" if r < 0.95 else random.choice(["6.2", "-1", "N/A"])))
    upd = atualizado or v["atualizado"]
    return [sujar_id(v["id"], "VND"), nome_out, razao, fmt_cnpj(v["cnpj"]), email, fmt_tel(DDD[v["uf"]]),
            cidade, uf, cat_out, fmt_data(v["cadastro"]), st_out, nota_out, upd.strftime("%Y-%m-%d %H:%M:%S")]


linhas_v = [linha_vendedor(v) for v in vendedores]
# duplicatas exatas
for v_l in random.sample(linhas_v, 25):
    linhas_v.append(list(v_l))
# versões antigas/novas do mesmo vendedor (para dedup por updated_at)
for v in random.sample(vendedores, 40):
    antigo = v["atualizado"] - timedelta(days=random.randint(30, 400))
    linhas_v.append(linha_vendedor(v, atualizado=antigo, status=random.choice(["ativo", "inativo"])))
# linhas lixo
linhas_v.append([""] * len(V_COLS))
linhas_v.append(["", "Loja Teste", "LOJA TESTE LTDA", "", "teste@teste", "", "", "", "", "", "ativo", "", "2026-01-01 00:00:00"])
random.shuffle(linhas_v)

with open("vendedores.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(V_COLS)
    w.writerows(linhas_v)

# ---------------- PRODUTOS ----------------
# distribuição de cauda longa: poucos vendedores concentram muitos produtos
pesos_v = [random.paretovariate(1.3) if v["status"] != "suspenso" else 0.2 for v in vendedores]
P_COLS = ["product_id", "seller_id", "sku", "nome_produto", "categoria", "marca", "preco", "custo",
          "estoque", "peso", "ativo", "data_cadastro", "updated_at"]
produtos = []
for k in range(1, N_PROD + 1):
    v = random.choices(vendedores, pesos_v)[0]
    cat = v["cat"] if random.random() < 0.8 else random.choice(CAT_NOMES)
    _, itens, (pmin, pmax) = CATS[cat]
    item = random.choice(itens)
    marca = random.choice(MARCAS)
    nome = f"{item} {marca} {random.choice(VARIANTES)}"
    preco = round(random.uniform(pmin, pmax), 2)
    custo = round(preco * random.uniform(0.35, 0.75), 2)
    cadastro = v["cadastro"] + timedelta(days=random.randint(0, max(1, (hoje - v["cadastro"]).days)))
    produtos.append(dict(id=f"PRD-{k:06d}", vend=v, cat=cat, nome=nome, marca=marca, preco=preco, custo=custo,
                         cadastro=cadastro,
                         atualizado=datetime.combine(cadastro, datetime.min.time()) + timedelta(
                             days=random.randint(0, max(1, (hoje - cadastro).days)), seconds=random.randint(0, 86399))))

vend_ids = {v["id"] for v in vendedores}


def linha_produto(p, atualizado=None, preco=None):
    v = p["vend"]
    sid = v["id"]
    r = random.random()
    if r < 0.03:
        sid = f"VND-{random.randint(N_VEND + 1, N_VEND + 300):05d}"  # órfão
    elif r < 0.05:
        sid = ""
    sid = sujar_id(sid, "VND") if sid else sid
    sku = f"{p['marca'][:3].upper()}-{p['id'][-6:]}"
    nome = p["nome"]
    r = random.random()
    if r < 0.08:
        nome = nome.upper()
    elif r < 0.14:
        nome = f"  {nome}"
    elif r < 0.18:
        nome = sem_acento(nome).lower()
    elif r < 0.19:
        nome = ""
    cat_out = p["cat"] if random.random() < 0.65 else random.choice(CATS[p["cat"]][0])
    if random.random() < 0.02:
        cat_out = ""
    marca = p["marca"] if random.random() < 0.85 else (p["marca"].upper() if random.random() < 0.6 else "")
    pr = preco if preco is not None else p["preco"]
    preco_out = fmt_preco(pr)
    custo = p["custo"]
    r = random.random()
    custo_out = f"{custo:.2f}" if r < 0.8 else (f"{custo:.2f}".replace(".", ",") if r < 0.9 else ("" if r < 0.95 else f"{pr * random.uniform(1.1, 1.6):.2f}"))  # custo > preço
    est = random.choices([0, random.randint(1, 50), random.randint(51, 500)], [10, 55, 35])[0]
    r = random.random()
    est_out = str(est) if r < 0.88 else ("" if r < 0.92 else (str(-random.randint(1, 20)) if r < 0.96 else random.choice(["N/A", "sem estoque", "12.0"])))
    kg = round(random.uniform(0.05, 12), 3)
    r = random.random()
    if r < 0.55:
        peso_out = f"{kg}"
    elif r < 0.7:
        peso_out = f"{kg}".replace(".", ",")
    elif r < 0.82:
        peso_out = f"{int(kg * 1000)}g"
    elif r < 0.92:
        peso_out = f"{kg} kg"
    else:
        peso_out = ""
    at = v["status"] == "ativo" and random.random() < 0.92
    ativo_out = random.choice(["true", "S", "1", "Sim", "TRUE"] if at else ["false", "N", "0", "Não", "FALSE"])
    cad = p["cadastro"]
    if random.random() < 0.02:
        cad = date(2027, random.randint(1, 12), random.randint(1, 28))  # data futura
    upd = atualizado or p["atualizado"]
    return [sujar_id(p["id"], "PRD"), sid, sku, nome, cat_out, marca, preco_out, custo_out, est_out, peso_out,
            ativo_out, fmt_data(cad), upd.strftime("%Y-%m-%d %H:%M:%S")]


linhas_p = [linha_produto(p) for p in produtos]
for l in random.sample(linhas_p, 30):
    linhas_p.append(list(l))
for p in random.sample(produtos, 50):
    linhas_p.append(linha_produto(p, atualizado=p["atualizado"] - timedelta(days=random.randint(10, 300)),
                                  preco=round(p["preco"] * random.uniform(0.8, 1.2), 2)))
linhas_p.append([""] * len(P_COLS))
random.shuffle(linhas_p)

with open("produtos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(P_COLS)
    w.writerows(linhas_p)

print("vendedores:", len(linhas_v), "| produtos:", len(linhas_p))
