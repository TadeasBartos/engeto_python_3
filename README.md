# Projekt 3 - Engeto Python Akademie

## Autor
- **Jméno:** Tadeáš Bartoš
- **Email:** bartos.tadeas@live.com
- **GitHub:** @TadeasBartos

## Popis
Tento projekt je součástí Engeto Python Akademie. 
Cílem je scrapování volebních dat obcí v okrese a jejich uložení do CSV souboru podle jednotlivých stran a obcí.

## Spuštění v konzoli
python3 projekt_3.py <vstupní_url_okresu> <výstupní_soubor.csv>

### Výstup
Výstupem je soubor.csv, kde řádky jsou jednotlivé obce a sloupce jsou jednotlivé strany.

#### Obecná ukázka
code,location,registered,envelopes,valid,<strana1_název>,<stranaN_název>
<kód první obce>, <název_obce>, <počet_registrovaných_voličů>, <počet_odevzdaných_obálek>, <počet_platných_obálek>, <počet_hlasů_strany1>, <počet_hlasů_stranyN>
<další obec> -> <počet_hlasů_stranyN>

#### Konkrétní ukázky
code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Volte Pr.Blok www.cibulka.net,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Společ.proti výst.v Prok.údolí,Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,OBČANÉ 2011-SPRAVEDL. PRO LIDI,Unie H.A.V.E.L.,Referendum o Evropské unii,TOP 09,ANO 2011,Dobrá volba 2016,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů
500054,Praha 1,21 556,14 167,14 036,2770,9,13,657,12,1,774,392,514,41,6,241,14,44,2332,5,0,12,2783,1654,1,7,954,3,133,11,2,617,34
500224,Praha 10,79 964,52 277,51 895,8137,40,34,3175,50,17,2334,2485,1212,230,15,1050,35,67,9355,9,8,30,6497,10856,37,53,2398,12,477,69,53,2998,162

### Hlavní Funkce:
- Scraping všech volebních dat ze serveru volby.cz.
- Vstupem je odkaz na okres.
- Extrakce podrobných výsledků voleb pro každou obec.
- Uložení výsledků do CSV souboru, včetně účasti ve volbách, výsledků voleb a hlasů jednotlivých stran.

### Funkce v programu
- **scrape_odkaz(odkaz)**: vytvoří soup z daného odkazu
- **volbycz_odkaz_obec(hlavni_odkaz, iterator)**: vytváří odkazy pro jednotlivé obce na základě hlavního odkazu a iterátoru (šestimístného čísla obce)
- **td_cistic(class_string, polevka)**: funkce čistí text z tagu 'td'
- **req_file(jmeno_souboru)**: vytvoří soupit všech potřebných balíčků
- **vstup1_check(url)**: kontroluje, zda je odkaz předpokládaného tvaru
- **vstup2_check(file_name)**: kontroluje, zda je výstupní soubor předpokládaného tvaru
- **main(odkaz, vystupni_soubor)**: hlavní funkce, vstupem je odkaz na okres a jméno výstupního souboru z konzole

## Požadavky
Než spustíš skript, ujisti se, že máš nainstalovanou knihovnu pro scraping webových stránek.
K jejich instalaci použij následující příkaz:
pip install beautifulsoup