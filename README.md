# Wordslet: sovellus vieraan kielen sanojen opiskeluun

[sovellus herokussa](https://tikaso-wordslet.herokuapp.com/)

### Loppupalautus

Sovelluksen suunniteltujen päätoiminnallisuuksien pitäisi nyt olla kunnossa. Sovellukseen on luotu kaksi testikäyttäjää ja testisanakokoelmia, joita voi käyttää arvioinnissa. Käyttäjät ovat maija salasanalla maija1 ja kaaleppi salasanalla kaaleppi1.

##### Tunnetut viat
- formien tiedot eivät säily jos jonkin syötteistä on virheellinen
- kokoelmakohtaisissa tilastoissa voi olla Noneja jos tilastoja ei vielä ole
- omista kokoelmista ei käy helposti ilmi onko se yksityinen vai julkinen ilman että menee muokkaamaan kokoelmaa
- koodissa on jonkun verran toisteisuutta
- funktiot on isoja
- sovelluksen ulkoasu on melko yksinkertainen

#### 07.08.2022

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
- [x] sanojen määrä
- [x] kokoelman luonut käyttäjä
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
