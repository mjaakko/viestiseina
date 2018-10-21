## Käyttötapaukset

### Kirjautumattomana käyttäjänä

* ...haluan rekisteröityä 
  * `INSERT INTO account (name, password) VALUES ("demo", "demo")`
  * `INSERT INTO user_role (user_id, role_id) VALUES (1, 1)`
* ...haluan kirjautua sisään
  * `SELECT account.id AS account_id, account.name AS account_name, account.password AS account_password FROM account WHERE account.name = "demo" AND account.password = "demo" LIMIT 1`
* ...haluan selata viestejä
  * `SELECT post.id AS post_id, post.parent_id AS post_parent_id, post.create_time AS post_create_time, post.modify_time AS post_modify_time, post.user_id AS post_user_id, post.content AS post_content FROM post WHERE post.parent_id IS NULL ORDER BY post.create_time DESC`
* ...haluan hakea viestejä
  * `SELECT post.id AS post_id, post.parent_id AS post_parent_id, post.create_time AS post_create_time, post.modify_time AS post_modify_time, post.user_id AS post_user_id, post.content AS post_content FROM post JOIN account ON account.id = post.user_id WHERE (post.content LIKE "viesti") AND account.name = "demo" ORDER BY post.create_time DESC`

### Kirjautuneena käyttäjänä

* ...haluan kirjoittaa viestejä
  * `INSERT INTO post (parent_id, create_time, modify_time, user_id, content) VALUES (null, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1, "viesti")`
* ...haluan päivittää kirjoittamiani viestejä
  * `UPDATE post SET modify_time=CURRENT_TIMESTAMP, content="päivitetty viesti" WHERE post.id = 1`
* ...haluan poistaa kirjoittamiani viestejä
  * `DELETE FROM post WHERE post.id = 1`
* ...haluan vastata viesteihin
  * `INSERT INTO post (parent_id, create_time, modify_time, user_id, content) VALUES (1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1, "vastaus")`
  * Viestin vastauksien määrä selviää kyselyllä:  
  ``` 
  WITH RECURSIVE replies AS (SELECT id, parent_id, id as root_id FROM post WHERE root_id IS :post_id UNION ALL SELECT c.id, c.parent_id, p.root_id FROM post c JOIN replies p ON c.parent_id = p.id) SELECT root_id AS post_id, count(*) AS reply_count FROM replies WHERE id <> root_id
  ```
* ...haluan selata suositumpia hashtageja
  * `SELECT hashtag.id, hashtag.name, COUNT(hashtag.id) FROM hashtag, post_hashtag, post WHERE hashtag.id = post_hashtag.hashtag_id AND post_hashtag.post_id = post.id GROUP BY hashtag.id ORDER BY COUNT(hashtag.id) DESC`
* ...haluan selata viestejä hashtagien perusteella
  * `SELECT post.id AS post_id, post.parent_id AS post_parent_id, post.create_time AS post_create_time, post.modify_time AS post_modify_time, post.user_id AS post_user_id, post.content AS post_content FROM post WHERE EXISTS (SELECT 1 FROM post_hashtag, hashtag WHERE post.id = post_hashtag.post_id AND hashtag.id = post_hashtag.hashtag_id AND hashtag.id = ?) ORDER BY post.create_time DESC`
* ...haluan mahdollisuuden vaihtaa salasanani
  * `UPDATE account SET password="salasana" WHERE account.id = 1`

### Moderaattorina

* ...haluan mahdollisuuden muiden poistaa viestejä
  * `DELETE FROM post WHERE post.id = 1`
* ...haluan mahdollisuuden muokata muiden viestejä
  * `UPDATE post SET modify_time=CURRENT_TIMESTAMP, content="päivitetty viesti" WHERE post.id = 1`

### Ylläpitäjänä

* ...haluan mahdollisuuden poistaa käyttäjiä
  * `DELETE FROM account WHERE accountz.id = 1`
* ...haluan tehdä käyttäjästä moderaattorin
  * `INSERT INTO user_role (user_id, role_id) VALUES (1, 2)`
* ...haluan poistaa käyttäjältä moderaattorin oikeudet
  * `DELETE FROM user_role WHERE user_role.user_id = 1 AND user_role.role_id = 2`
