## Vaatimukset

Python 3.7+ (eli uudempi kuin python versio 3.7)
```
https://www.python.org/downloads/
```
Python.exe tulee olla asetettu PATH-järjestelmämuuttujiin.

### Ongelmatilanne 
Windows tarjoaa windows-storea kun kirjoitat python.exe komentokehoitteeseen

1. Käynnistä
2. "Manage app execution aliases"
3. Etsi "App installer" joka osoittaa python.exe tai python3.exe
4. Aseta pois käytöstä.

## Twitchio library:

Etsi pythonin asennuspolku esimerkiksi default asennuksena tehdyllä

```
1. Avaa CMD
2. cd C:\Users\<käyttäjänimi>\AppData\Local\Programs\Python\Python39
3. python -m pip install twitchio
```

Tämä komento asentaa käyttämällä pythonin PIP pakettienhallintaa botin tarvitseman frameworkin

## Twitch IRC access token:

Tätä tarvitaan, jotta voidaan yhdistää twitch.tv:n chattiin.

1. Kirjaudu käyttäjällä, jolla haluat botin toimivan alla olevalle sivustolle, anna valtuutus ja saat sivusto generoi sinulle oauth tunnuksen.
2. Aseta oauth TMI_TOKEN ympäristömuuttujaan

```
https://twitchapps.com/tmi/
```

## Asennus

1. Avaa komentokehoite (CMD.exe)
2. Syötä komennot
3. Komennot mallissa setx <muuttujanimi> <välilyönti> <asetettava muuttuja>

Asetetaan oauth
```
SETX TMI_TOKEN <TWITCH IRC TOKEN>
```
Prefix josta tunnistetaan mikä on komento ja mikä ei (!aloita !sulje) jne. 
```
SETX BOT_PREFIX !
```
Kanava jolle botti yhdistää käynnistyessään
```
SETX CHANNEL <kanava>
```

Nämä muuttujat botti tarvitsee toimiakseen, voit myös asettaa nämä myös käyttämällä windowsin ympäristömuuttujat valikkoa jos komentokehoitteen käyttäminen ei maistu.

3. Copy&pastee tai kloonaa main.py tästä repositorystä ja tallenna (muista .py pääte).

## Botin käynnistys
1. Avaa CMD ja siirry kansioon jonne tallensit koodin
2. Kirjoita tiedostonnimi, jolla tallensit koodipätkän. (esimerkiksi jos kloonasit repon niin main.py TAI jos kopioit ja tallensit toisella nimellä niin tämän tiedoston nimi)
3. Paina enter
4. Jos kaikki meni hyvin botti ilmoittaa ikkunassa millä tunnuksilla se on kirjautunut sisään ja statuksensa
