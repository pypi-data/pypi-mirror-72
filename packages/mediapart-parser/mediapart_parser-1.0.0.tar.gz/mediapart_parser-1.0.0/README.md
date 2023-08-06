# Mediapart Parser
  
[![Unit tests](https://github.com/r0perice/mediapart-parser/workflows/Unit%20tests/badge.svg)](https://github.com/r0perice/mediapart-parser/actions?query=workflow%3A%22Unit+tests%22)
 
# Quick Start
```python
pip install mediapart-parser
```

```python
from mediapart_parser import MediapartParser
parser = MediapartParser(mediapart_user_name, mediapart_user_password)
```
With:
* `mediapart_user_name`: a String containing your Mediapart's user name.
* `mediapart_user_password`: a String containing you Mediapart's password.

# Usage
#### Get last 10 articles links from RSS feed

```python
>>> parser.get_last_articles_links()
```
 Result looks like
>['https://www.mediapart.fr/journal/france/260620/affaire-kohler-l-ardoise-de-msc-s-eleve-26-milliards-d-euros-pour-l-etat', 'https://www.mediapart.fr/journal/france/260620/lille-martine-aubry-joue-son-va-tout-sur-les-quartiers-populaires', 'https://www.mediapart.fr/journal/france/260620/un-policier-de-la-bac-condamne-bayonne-lors-du-proces-du-lbd', 'https://www.mediapart.fr/journal/france/260620/violation-reiteree-du-confinement-le-conseil-constitutionnel-valide', 'https://www.mediapart.fr/journal/france/260620/grande-distribution-la-concurrence-ne-concerne-pas-l-outre-mer', 'https://www.mediapart.fr/journal/france/260620/sarkozy-et-des-avocats-s-indignent-d-avoir-ete-espionnes', 'https://www.mediapart.fr/journal/france/260620/affaire-vassal-une-candidate-de-l-equipe-lr-autorisee-recueillir-des-procurations', 'https://www.mediapart.fr/journal/france/260620/au-proces-du-djihadiste-tyler-vilus-quand-organise-une-execution', 'https://www.mediapart.fr/journal/france/260620/les-travailleurs-les-plus-exposes-au-covid-19-ont-aussi-ete-les-moins-proteges-par-leur-entreprise', 'https://www.mediapart.fr/journal/culture-idees/260620/miseres-et-vertus-du-rituel-electoral']

#### Get last 10 articles titles from RSS feed
```python
>>> parser.get_last_articles_titles()
```
Result looks like
>['Affaire Kohler: l’ardoise de MSC s’élève à 2,6 milliards d’euros pour l’Etat', 'A Lille, Martine Aubry joue son «va-tout» sur les quartiers populaires', 'Un policier de la BAC condamné à Bayonne lors du «procès du 
LBD»', '«Violation réitérée du confinement»: le Conseil constitutionnel valide', 'Grande distribution: la concurrence ne concerne pas l’Outre-mer', 'Sarkozy et des avocats s’indignent d’avoir été espionnés', 'Affaire Vassal: une candidate de l’équipe LR autorisée à recueillir des procurations', 'Au procès du djihadiste Tyler Vilus: «Quand on organise une exécution...»', 'Les travailleurs les plus exposés au Covid-19 ont aussi été les 
moins protégés par leur entreprise', 'Misères et vertus du rituel électoral']
 
#### Get last 10 articles categories from RSS feed
```python
>>> parser.get_last_articles_categories()
```
Result looks like
>["CONFLITS D'INTÉRÊTS", 'GAUCHE(S)', 'Violences policières', 'Société', 'outre-mer', 'Note de veille', 'Enquête', 'Terrorisme', 'SOCIAL', 'POLITIQUE']

#### Get article identifier
```python
>>> parser.get_article_id(string: article_url)
```
Result looks like
>893104

#### Download article
```python
>>> parser.download_article(string: article_id, string: file_path)
```

