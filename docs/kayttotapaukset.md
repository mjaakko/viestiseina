## Käyttötapaukset

### Käyttäjänä

* ...haluan selata viestejä
* ...haluan kirjoittaa viestejä
* ...haluan päivittää kirjoittamiani viestejä
* ...haluan poistaa kirjoittamiani viestejä
* ...haluan vastata viesteihin
* ...haluan selata suositumpia hashtageja
  * `SELECT hashtag.id, hashtag.name, COUNT(hashtag.id) FROM hashtag, 
post_hashtag WHERE hashtag.id = post_hashtag.hashtag_id GROUP BY 
hashtag.id ORDER BY COUNT(hashtag.id) DESC`
* ...haluan selata viestejä hashtagien perusteella

### Moderaattorina

* ...haluan mahdollisuuden muiden poistaa viestejä
* ...haluan mahdollisuuden muokata muiden viestejä

### Ylläpitäjänä

* ...haluan mahdollisuuden poistaa käyttäjiä
* ...haluan tehdä käyttäjästä moderaattorin
