# Wordslet: sovellus vieraan kielen sanojen opiskeluun

#### 07.08.2022

https://tikaso-wordslet.herokuapp.com/

Herokussa voi luoda uuden käyttäjän, kirjautua sovellukseen ja tehdä oman sanakokoelman, joka näkyy käyttäjän omilla sivuilla. Luotuja kokoelmia voi myös poistaa. Tällä hetkellä muokkauksesta toimii vain yksitäisten sanojen poisto. Käyttäjiä voi myös hakea hakupalkista.

## Käyttö
Sovelluksella voi harjoitella esimerkiksi vieraan kielen sanoja. Sovellusta voi käyttää normaalina käyttäjänä tai tähtikäyttäjänä. Sanakokoelmia voi hakea niiden nimellä tai ne luoneen käyttäjän nimellä.

- [x] sovellukseen voi luoda uuden käyttäjän
- [x] sovellukseen voi kirjautua olemassaolevana käyttäjänä

Käyttäjä voi
- [x] luoda oman sanakokoelman
- [x] lisätä olemassaoleviin sanakokoelmiin uusia sanoja
- [x] poistaa kokoelmasta sanoja
- [x] harjoitella sanakokoelmia
- [x] muokata kokoelman sanoja
- [x] poistaa kokoelman

Kirjautumaton käyttäjä voi selata käyttäjiä ja sanakokoelmia, mutta ei harjoitella niitä.

## Sanakokoelmat
Sanakokoelmista näkyvät tiedot:
- [x] nimi (pakollinen)
- [ ] sanojen määrä
- [ ] kokoelman luonut käyttäjä
- [x] käyttäjän kirjoittama kuvaus (vapaaehtoinen)

Sanakokoelma voi olla julkinen tai yksityinen.

## Sanojen harjoittelu
- [x] harjoittelutilassa käyttäjä saa kokoelmasta satunnaisia sanoja käännettäväksi
- [x] käyttäjä kirjoittaa saamalleen sanalle käännöksen ja saa palautteen, meneekö se oikein
- [x] harjoittelu päättyy kun kaikki sanat on käyty läpi (tai jos käyttäjä haluaa keskeyttää harjoittelun)
- [x] harjoittelun jälkeen käyttäjä saa näkyviin sanat ja tiedon siitä kuinka monella arvauksella sanan sai oikein
- [ ] käyttäjä näkee jokaisen oman kokoelman kohdalla kuinka monta kertaa on harjoitellut sitä

## Jos aikaa jää:
- mahdollisuus tallentaa kokoelmia tai tykätä niistä

- normaalikäyttäjän lisäksi tähtikäyttäjä, joka voi
    - tehdä kaiken mitä normaalikäyttäjäkin
    - luoda ryhmän normaalikäyttäjille
    - jakaa ryhmälle yhden tai useamman sanakokoelman harjoiteltavaksi
    - seurata käyttäjäkohtaisia tilastoja ryhmässä
