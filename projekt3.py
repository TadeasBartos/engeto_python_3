"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Tadeáš Bartoš
email: bartos.tadeas@live.com
github: @TadeasBartos
"""

import sys
import subprocess
import requests
import csv
from bs4 import BeautifulSoup as bs

def scrape_odkaz(odkaz: str) -> bs:
    """
    Funkce scrapuje odkaz.

    Parametry:
    -----------------------
    odkaz - odkaz, který se má scrapovat

    Vrací:
    -----------------------
    soup - soup objekt, který obsahuje informace z odkazu
    
    """
    odpoved_serveru = requests.get(odkaz)
    soup = bs(odpoved_serveru.text, 'html.parser')
    return soup

def volbycz_odkaz_obec(hlavni_odkaz: str, iterator: int) -> str:
    """
    Funkce vytváří odkaz pro každou obec na základě odkazu šestimístného číslo obce.

    Parametry:
    -----------------------
    hlavni_odkaz - odkaz na okres
    iterator - šestimístné číslo obce z listu obce_cisla_list

    Vrací:
    -----------------------
    odkaz - odkaz na obec
    """
    koncovka = hlavni_odkaz[-4:]
    odkaz = hlavni_odkaz.replace("/ps32?", "/ps311?")
    odkaz = odkaz[:-14]
    konec_odkazu = "&xobec=" + str(iterator) + "&xvyber=" + str(koncovka)
    odkaz = odkaz + konec_odkazu
    return odkaz

def td_cistic(class_string: str, polevka: bs) -> list:
    """
    Funkce čistí text z tagu td.

    Parametry:
    -----------------------
    class_string - třída tagu td
    polevka - soup objekt, který obsahuje informace z odkazu

    Vrací:
    -----------------------
    list - list s čistým textem z tag
    """
    return [td.get_text() for td in polevka.find_all("td", class_=class_string)]

def req_file(jmeno_souboru: str) -> None:
    """
    Funkce vytváří soubor s všech nainstalovaných balíčků.

    Parametry:
    -----------------------
    jmeno_souboru.txt - název výstupního souboru ve formátu .txt

    Vrací:
    -----------------------
    jmeno_souboru.txt - soubor s nainstalovanými balíčky
    """
    with open(jmeno_souboru, "w") as file:
        subprocess.run(["python3", "-m", "pip", "list"], stdout=file, check=True)

def vstup1_check(url: str) -> bool:
    """
    Funkce kontroluje, zda je odkaz správný.

    Parametry:
    -----------------------
    url - odkaz, který se má kontrolovat

    Vrací:
    -----------------------
    True/False
    """
    url_check = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&x"
    return url_check in url

def vstup2_check(file_name: str) -> bool:
    """
    Funkce kontroluje, zda je formát výstupu správný.

    Parametry:
    -----------------------
    file_name - název souboru, který se má kontrolovat

    Vrací:
    -----------------------
    True/False
    """
    return file_name.endswith(".csv")

def main(odkaz: str, vystupni_soubor: str) -> csv:
    """
    Hlavní funkce programu, která scrapuje data a ukládá je do csv souboru.

    Parametry:
    -----------------------
    odkaz - odkaz na okres, tyto obce se budou scrapovat
    vystupni_soubor - název výstupního souboru ve formátu .csv

    Vrací:
    -----------------------
    csv - výstupní soubor s daty

    Postup:
    1. Je vygenerován soubor všech potřebných knihoven k chodu funkcí req_file(jmeno_souboru).
    2. Je vytvořen zapisovač pro vytvoření finálního csv.
    3. Z funkce scrape_odkaz(odkaz) a td_cistic(class_string, polevka) jsou získány listy obce_jmena_list a obce_cisla_list.
    4. Hlavní cyklus prochází jednotlivé obce:
        4.1. Pro každou obec je vytvořen odkaz a získán soup objekt.
        4.2. Jsou získány jednotlivé řádky tabulky.
        4.3. Jsou získány první sloupce řádku: číslo a jméno obce.
        4.4. Jsou získány informace o účasti a výsledcích voleb.
        4.5. Jsou získány informace o jednotlivých stranách.
        4.6. Při prvním průběhu cyklu je zapsána legenda tabulky z vytvořeného listu legenda_tabulky_strany.
        4.6. Jsou zapsány do csv souboru.
        4.7. "wash, rinse, repeat" všech obcí v okrese.
    """

    req_file("requirements.txt")

    vystup_csv = open(vystupni_soubor, mode="w", encoding="UTF-8", newline="")
    zapisovac = csv.writer(vystup_csv)

    obce_jmena_list = td_cistic("overflow_name", scrape_odkaz(odkaz))
    obce_cisla_list = td_cistic("cislo", scrape_odkaz(odkaz))

    legenda_tabulky_strany = []

    for strana in range(len(obce_jmena_list)):

        soup_obec = scrape_odkaz(volbycz_odkaz_obec(odkaz, obce_cisla_list[strana]))
        rows = soup_obec.find_all("tr")

        data_strany = []
        data_strany.extend([
            obce_cisla_list[strana],
            obce_jmena_list[strana]
        ])

        for row in rows:
            cols = row.find_all('td')

            if len(cols) >= 8:
                data_strany.extend([
                    cols[3].text.strip(),
                    cols[4].text.strip(),
                    cols[7].text.strip()
                ])

        for row in rows[4:]:
            cols = row.find_all("td")

            if len(cols) < 4:
                continue

            try:
                party_id = int(cols[0].text.strip())
            except ValueError:
                continue

            party_name = cols[1].text.strip()
            legenda_tabulky_strany.append(party_name)

            try:
                total_votes = int(cols[2].text.strip().replace("\xa0", "").replace(",", ""))
            except ValueError:
                total_votes = 0

            data_strany.append(total_votes)

        if strana == 0:
            legenda_tabulky = ["code", "location", "registered", "envelopes", "valid"] + legenda_tabulky_strany
            zapisovac.writerow(legenda_tabulky)

        zapisovac.writerow(data_strany)

    vystup_csv.close()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Nesprávný počet argumentů. Použití: script.py <vstupní_url> <výstupní_soubor.csv>")
        sys.exit(1)

    vstup1 = sys.argv[1]
    vstup2 = sys.argv[2]

    if not vstup1_check(vstup1):
        print("Nezadal jsi správný odkaz.")
        sys.exit(1)

    if not vstup2_check(vstup2):
        print("Nezadal jsi správný formát výstupu - musí končit na .csv.")
        sys.exit(1)

    try:
        main(vstup1, vstup2)
    except Exception as e:
        print(f"Došlo k chybě během vykonávání programu: {e}")
        sys.exit(1)