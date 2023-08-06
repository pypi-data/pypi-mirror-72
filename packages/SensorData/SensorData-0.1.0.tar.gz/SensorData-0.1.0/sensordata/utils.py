try:
   conn = mariadb.connect(
      user="sog",
      password="psog",
      host="localhost",
      port=3306)
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)

#Write Data to test.dht22log
def add_dht22entry(cur, phumidity, ptemperature):
   """Adds the given contact to the contacts table"""

   cur.execute("INSERT INTO test.dht22log(population_date, humidity, temperature) VALUES (now(), ?, ?)",
      (phumidity, ptemperature))