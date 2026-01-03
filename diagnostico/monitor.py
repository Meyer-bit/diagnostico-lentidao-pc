import psutil
import time 
from datetime import datetime
import os


# configurações iniciais
max_cpu = 80
max_ram = 85
min_leituras = 3
intervalo = 5


# sistema
leituras_lentas = 0
leituras_normais = 0
em_lentidao = False
processos_suspeitos = []

cpu_soma = 0
ram_soma = 0
leituras_evento = 0


# função para obter os processos que mais consomem recursos
def top_processos():
    lista = []

    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            lista.append({
                'nome': proc.info['name'],
                'cpu': proc.info['cpu_percent'],
                'ram': proc.info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    lista.sort(key=lambda p: (p['cpu'], p['ram']), reverse=True)
    return lista[:5]


# função para explicar a lentidão
def explicar_lentidao(duracao, processos, cpu_media, ram_media):
    explicacao = []

    if ram_media > cpu_media:
        explicacao.append(
            "A lentidão foi causada principalmente pelo alto uso de memória RAM."
        )
    else:
        explicacao.append(
            "A lentidão foi causada principalmente pelo alto uso da CPU."
        )

    explicacao.append(
        f"Os programas mais envolvidos foram: {', '.join(processos)}."
    )

    explicacao.append(
        f"A lentidão durou aproximadamente {duracao}."
    )

    explicacao.append(
        "Sugestão: feche programas não utilizados ou evite abrir muitos aplicativos ao mesmo tempo."
    )

    return " ".join(explicacao)


# criação das pastas
os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)


# loop principal
while True:
    cpu = psutil.cpu_percent()
    memoria = psutil.virtual_memory()
    ram = memoria.percent
    agora = datetime.now()


    # detecção de lentidão
    if cpu >= max_cpu or ram >= max_ram:
        leituras_lentas += 1
        leituras_normais = 0
    else:
        leituras_normais += 1
        leituras_lentas = 0


    # início da lentidão
    if leituras_lentas >= min_leituras and not em_lentidao:
        em_lentidao = True
        inicio_lentidao = agora
        processos_suspeitos.clear()
        cpu_soma = 0
        ram_soma = 0
        leituras_evento = 0

        print(f"[{agora}] ALERTA: Sistema em lentidão! CPU: {cpu}%, RAM: {ram}%")


    # coleta durante a lentidão
    if em_lentidao:
        cpu_soma += cpu
        ram_soma += ram
        leituras_evento += 1
        processos_suspeitos.extend(top_processos())


    # fim da lentidão
    if em_lentidao and leituras_normais >= min_leituras:
        em_lentidao = False
        fim_lentidao = agora
        duracao = fim_lentidao - inicio_lentidao

        cpu_media = cpu_soma / leituras_evento
        ram_media = ram_soma / leituras_evento


        # agrupa processos
        contagem = {}
        for proc in processos_suspeitos:
            nome = proc['nome']
            contagem[nome] = contagem.get(nome, 0) + 1

        principais_processos = [
            nome for nome, _ in sorted(
                contagem.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
        ]

        explicacao = explicar_lentidao(
            duracao,
            principais_processos,
            cpu_media,
            ram_media
        )

        print(f"[{agora}] INFO: Sistema voltou ao normal. Duração: {duracao}")
        print("\n Diagnóstico:")
        print(explicacao)


        # geração do relatório
        with open("reports/relatorio.txt", "a", encoding="utf-8") as rel:
            rel.write("==== RELATÓRIO DE LENTIDÃO ====\n")
            rel.write(f"Início: {inicio_lentidao}\n")
            rel.write(f"Fim: {fim_lentidao}\n")
            rel.write(f"Duração: {duracao}\n")
            rel.write(f"CPU média: {cpu_media:.2f}%\n")
            rel.write(f"RAM média: {ram_media:.2f}%\n")
            rel.write(f"Processos: {', '.join(principais_processos)}\n")
            rel.write(f"Diagnóstico: {explicacao}\n\n")


    # log contínuo
    print(f"{agora} | CPU: {cpu}% | RAM: {ram}%")

    with open("data/logs.csv", "a") as arquivo:
        arquivo.write(f"{agora},{cpu},{ram}\n")

    time.sleep(intervalo)
