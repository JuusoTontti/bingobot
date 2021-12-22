# bingobot

Vaatimukset

Python 3.7+ (eli uudempi kuin python versio 3.7)
```
https://www.python.org/downloads/
```
Python.exe tulee olla asetettu PATH-järjestelmämuuttujiin.

Jos windows tarjoaa windows-storea kun kirjoitat python.exe komentokehoitteeseen

1. Käynnistä
2. "Manage app execution aliases"
3. Etsi "App installer" joka osoittaa python.exe tai python3.exe
4. Aseta pois käytöstä.

Twitchio library:

Etsi pythonin asennuspolku esimerkiksi default asennuksena tehdyllä

```
1. Avaa CMD
2. cd C:\Users\<käyttäjänimi>\AppData\Local\Programs\Python\Python39
3. python -m pip install twitchio
```

Tämä komento asentaa käyttämällä pythonin PIP pakettienhallintaa botin tarvitseman frameworkin

Twitch IRC access token:

Tätä tarvitaan, jotta voidaan yhdistää twitch.tv:n chattiin.

```
https://twitchapps.com/tmi/
```



Asennus

1. Avaa komentokehoite (CMD.exe)
2. Syötä komento
```
SET TMI_TOKEN=<TWITCH IRC TOKEN>
SET BOT_PREFIX=!
SET CHANNEL=<kanava jolle botti yhdistää käynnistyessään>
```
Nämä muuttujat botti tarvitsee toimiakseen, voit myös asettaa nämä myös käyttämällä windowsin ympäristömuuttujat valikkoa jos komentokehoitteen käyttäminen ei maistu.
