# Viestiseinä

Sovellus Helsingin yliopiston kurssille Tietokantasovellus (2018).

Viestiseinälle on mahdollista kirjoittaa viestejä ja vastata muiden 
viesteihin.

* [Sovellus Herokussa](https://viestiseina-tsoha.herokuapp.com/)
  * Testikäyttäjä: **demo**, salasana: **demo**
  * Testikäyttäjä ylläpitäjän oikeuksin: **admin**, salasana: **admin**

## Dokumentaatio

* [Yleinen dokumentaatio](docs/yleinen.md)
  * Sovelluksen rajoitteet ja puutteet, omat kokemukset
* [Asennusohje](docs/asennusohje.md)
* [Käyttöohje](docs/kayttoohje.md)
* [Tietokannan rakenne](docs/tietokantarakenne.md)
* [Käyttötapaukset](docs/kayttotapaukset.md)

## Käyttö Dockerilla

`docker run -d -p 8000:8000 mjaakko/viestiseina`
