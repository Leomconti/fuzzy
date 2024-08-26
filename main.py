import csv
from typing import Dict, List


class FuzzyVariable:
    """
    Igual a implementacao java
    """

    def __init__(self, name: str, b1: float, t1: float, t2: float, b2: float):
        self.name = name
        self.b1 = b1
        self.t1 = t1
        self.t2 = t2
        self.b2 = b2

    def fuzzify(self, v: float) -> float:
        if v < self.b1 or v > self.b2:
            return 0.0
        if self.t1 <= v <= self.t2:
            return 1.0
        if self.b1 < v < self.t1:
            return (v - self.b1) / (self.t1 - self.b1)
        if self.t2 < v < self.b2:
            return 1.0 - ((v - self.t2) / (self.b2 - self.t2))
        return 0.0


class FuzzyVariableGroup:
    """
    Igual a implementacao java
    """

    def __init__(self, name: str, universe: List[float]):
        self.name = name
        self.universe = universe
        self.variables: Dict[str, FuzzyVariable] = {}

    def add_variable(self, var: FuzzyVariable):
        self.variables[var.name] = var

    def list_variables(self):
        return list(self.variables.keys())

    def fuzzify(self, v: float) -> Dict[str, float]:
        return {var_name: var.fuzzify(v) for var_name, var in self.variables.items()}


def read_csv(filename: str) -> List[Dict[str, str]]:
    data = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def apply_rule_and(as_variaveis: Dict[str, float], var1: str, var2: str, varr: str):
    """
    Aplicacao da regra AND
    """
    v = min(as_variaveis.get(var1, 0), as_variaveis.get(var2, 0))
    as_variaveis[varr] = max(as_variaveis.get(varr, 0), v)


# Processa a linha do csv de acordo com as regras e variaveis fuzzy q a gnt definiu
def process_row(
    row: Dict[str, str],
    grupo_popularity: FuzzyVariableGroup,
    grupo_revenue: FuzzyVariableGroup,
    grupo_runtime: FuzzyVariableGroup,
    grupo_vote_average: FuzzyVariableGroup,
    rules: List[Dict[str, str]],
) -> float:
    as_variaveis = {}

    try:
        popularity = float(row["popularity"])
        revenue = float(row["revenue"])
        runtime = float(row["runtime"])
        vote_average = float(row["vote_average"])
    except Exception:
        return 0

    as_variaveis.update(grupo_popularity.fuzzify(popularity))
    as_variaveis.update(grupo_revenue.fuzzify(revenue))
    as_variaveis.update(grupo_runtime.fuzzify(runtime))
    as_variaveis.update(grupo_vote_average.fuzzify(vote_average))

    # Apply fuzzy logic rules
    for rule in rules:
        apply_rule_and(as_variaveis, rule["var1"], rule["var2"], rule["varr"])

    NA = as_variaveis.get("NA", 0)
    A = as_variaveis.get("A", 0)
    MA = as_variaveis.get("MA", 0)
    if NA + A + MA > 0:
        score = (NA * 1.5 + A * 7.0 + MA * 9.5) / (NA + A + MA)
    else:
        score = 0

    return score


def define_rule_sets():
    """
    Para ter um output legal, a gente definiu algumas regras "de negócio"
    para dar scores em diferentes áreas do cinema, já que pegamos várias variáveis.
    """
    regras_comercial = [
        {"var1": "Popular", "var2": "Hit", "varr": "A"},
        {"var1": "Extremamente Popular", "var2": "Blockbuster", "varr": "MA"},
        {"var1": "Fracasso", "var2": "Impopular", "varr": "NA"},
    ]

    regras_critica = [
        {"var1": "Excelente", "var2": "Muito Longo", "varr": "MA"},
        {"var1": "Bom", "var2": "Médio", "varr": "A"},
        {"var1": "Ruim", "var2": "Curto", "varr": "NA"},
    ]

    regras_audiencia = [
        {"var1": "Popular", "var2": "Longo", "varr": "A"},
        {"var1": "Extremamente Popular", "var2": "Muito Longo", "varr": "MA"},
        {"var1": "Impopular", "var2": "Curto", "varr": "NA"},
    ]

    regras_geral = [
        {"var1": "Popular", "var2": "Bom", "varr": "A"},
        {"var1": "Extremamente Popular", "var2": "Blockbuster", "varr": "MA"},
        {"var1": "Fracasso", "var2": "Ruim", "varr": "NA"},
        {"var1": "Hit", "var2": "Excelente", "varr": "MA"},
        {"var1": "Normal", "var2": "Médio", "varr": "A"},
    ]

    return {
        "comercial": regras_comercial,
        "critico": regras_critica,
        "audiencia": regras_audiencia,
        "geral": regras_geral,
    }


def calculate_score(row, grupo_popularidade, grupo_receita, grupo_duracao, grupo_nota_media, rules):
    # Calcular uma pontuação para um conjunto específico de regras
    score = process_row(row, grupo_popularidade, grupo_receita, grupo_duracao, grupo_nota_media, rules)
    return score


def run_fuzzy():
    # POPULARITY
    extremamente_popular = FuzzyVariable("Extremamente Popular", 48.82, 48.82, 875.58, 875.58)
    popular = FuzzyVariable("Popular", 12.92, 12.92, 48.82, 875.58)
    normal = FuzzyVariable("Normal", 1.28, 1.28, 12.92, 48.82)
    impopular = FuzzyVariable("Impopular", 0, 0, 1.28, 12.92)

    grupo_popularidade = FuzzyVariableGroup("Popularidade", [0, 875.58])
    grupo_popularidade.add_variable(extremamente_popular)
    grupo_popularidade.add_variable(popular)
    grupo_popularidade.add_variable(normal)
    grupo_popularidade.add_variable(impopular)

    # REVENUE
    blockbuster = FuzzyVariable("Blockbuster", 227634600, 227634600, 2787965087, 2787965087)
    hit = FuzzyVariable("Hit", 82260640, 82260640, 227634600, 2787965087)
    media = FuzzyVariable("Média", 19170000, 19170000, 82260640, 227634600)
    fracasso = FuzzyVariable("Fracasso", 0, 0, 19170000, 82260640)

    grupo_receita = FuzzyVariableGroup("Receita", [0, 2787965087])
    grupo_receita.add_variable(blockbuster)
    grupo_receita.add_variable(hit)
    grupo_receita.add_variable(media)
    grupo_receita.add_variable(fracasso)

    # RUNTIME
    muito_longo = FuzzyVariable("Muito Longo", 132, 132, 338, 338)
    longo = FuzzyVariable("Longo", 103, 103, 132, 338)
    medio = FuzzyVariable("Médio", 87, 87, 103, 132)
    curto = FuzzyVariable("Curto", 0, 0, 87, 103)

    grupo_duracao = FuzzyVariableGroup("Duração", [0, 338])
    grupo_duracao.add_variable(muito_longo)
    grupo_duracao.add_variable(longo)
    grupo_duracao.add_variable(medio)
    grupo_duracao.add_variable(curto)

    # VOTE AVERAGE
    excelente = FuzzyVariable("Excelente", 7.3, 7.3, 10, 10)
    bom = FuzzyVariable("Bom", 6.2, 6.2, 7.3, 10)
    media_nota = FuzzyVariable("Média", 4.9, 4.9, 6.2, 7.3)
    ruim = FuzzyVariable("Ruim", 0, 0, 4.9, 6.2)

    grupo_nota_media = FuzzyVariableGroup("Nota Média", [0, 10])
    grupo_nota_media.add_variable(excelente)
    grupo_nota_media.add_variable(bom)
    grupo_nota_media.add_variable(media_nota)
    grupo_nota_media.add_variable(ruim)

    rule_sets = define_rule_sets()

    data = read_csv("movie_dataset.csv")

    results = []
    for row in data:
        # Pegar os valores originais para usarmos no relatorio
        try:
            original_popularity = float(row["popularity"])
            original_revenue = float(row["revenue"])
            original_runtime = float(row["runtime"])
            original_vote_average = float(row["vote_average"])
        except Exception:
            # Excecao da quando o valor eh nulo ou '', entao a gnt so pula a linha
            continue

        # Calcular scores de acordo com as regras que definimos
        score_comercial = calculate_score(
            row, grupo_popularidade, grupo_receita, grupo_duracao, grupo_nota_media, rule_sets["comercial"]
        )
        score_critico = calculate_score(
            row, grupo_popularidade, grupo_receita, grupo_duracao, grupo_nota_media, rule_sets["critico"]
        )
        score_audiencia = calculate_score(
            row, grupo_popularidade, grupo_receita, grupo_duracao, grupo_nota_media, rule_sets["audiencia"]
        )
        score_geral = calculate_score(
            row, grupo_popularidade, grupo_receita, grupo_duracao, grupo_nota_media, rule_sets["geral"]
        )

        # guardamos tudo em um dicionario para pegar e montar o relatorio no final
        results.append(
            {
                "title": row["title"],
                "score_comercial": score_comercial,
                "score_critico": score_critico,
                "score_audiencia": score_audiencia,
                "score_geral": score_geral,
                "original_popularity": original_popularity,
                "original_revenue": original_revenue,
                "original_runtime": original_runtime,
                "original_vote_average": original_vote_average,
            }
        )

        # Print dos valores original + score geral
        print(f"Filme: {row['title']}")
        print(
            f"Popularidade: {original_popularity:.2f}, Receita: {original_revenue:.2f}, Duração: {original_runtime:.2f}, Nota Média: {original_vote_average:.2f}"
        )
        print(
            f"Score Comercial: {score_comercial:.2f}, Score Crítico: {score_critico:.2f}, Score Audiência: {score_audiencia:.2f}, Score Geral: {score_geral:.2f}\n"
        )

    # Extra:
    # Pegar top10 por categoria e fazer o print
    top_10_comercial = sorted(results, key=lambda x: x["score_comercial"], reverse=True)[:10]
    top_10_critico = sorted(results, key=lambda x: x["score_critico"], reverse=True)[:10]
    top_10_audiencia = sorted(results, key=lambda x: x["score_audiencia"], reverse=True)[:10]
    top_10_geral = sorted(results, key=lambda x: x["score_geral"], reverse=True)[:10]

    print("\nTop 10 Filmes por Score Comercial:")
    for result in top_10_comercial:
        print(f"{result['title']}: Score Comercial: {result['score_comercial']:.2f}")

    print("\nTop 10 Filmes por Score Crítico:")
    for result in top_10_critico:
        print(f"{result['title']}: Score Crítico: {result['score_critico']:.2f}")

    print("\nTop 10 Filmes por Score de Audiência:")
    for result in top_10_audiencia:
        print(f"{result['title']}: Score de Audiência: {result['score_audiencia']:.2f}")

    print("\nTop 10 Filmes por Score Geral:")
    for result in top_10_geral:
        print(f"{result['title']}: Score Geral: {result['score_geral']:.2f}")

    return results


def generate_report(results, filename="relatorio.md"):
    with open(filename, "w") as file:
        file.write("\n# Top 10 Filmes por Categoria\n")

        top_10_comercial = sorted(results, key=lambda x: x["score_comercial"], reverse=True)[:10]
        top_10_critico = sorted(results, key=lambda x: x["score_critico"], reverse=True)[:10]
        top_10_audiencia = sorted(results, key=lambda x: x["score_audiencia"], reverse=True)[:10]
        top_10_geral = sorted(results, key=lambda x: x["score_geral"], reverse=True)[:10]

        file.write("\n## Top 10 Filmes por Score Comercial:\n")
        for result in top_10_comercial:
            file.write(f"- {result['title']}: Score Comercial: {result['score_comercial']:.2f}\n")

        file.write("\n## Top 10 Filmes por Score Crítico:\n")
        for result in top_10_critico:
            file.write(f"- {result['title']}: Score Crítico: {result['score_critico']:.2f}\n")

        file.write("\n## Top 10 Filmes por Score de Audiência:\n")
        for result in top_10_audiencia:
            file.write(f"- {result['title']}: Score de Audiência: {result['score_audiencia']:.2f}\n")

        file.write("\n## Top 10 Filmes por Score Geral:\n")
        for result in top_10_geral:
            file.write(f"- {result['title']}: Score Geral: {result['score_geral']:.2f}\n")


if __name__ == "__main__":
    results = run_fuzzy()
    generate_report(results)
