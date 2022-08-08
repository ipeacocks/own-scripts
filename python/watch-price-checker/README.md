# Watch Price Checker

Build and run:
```
$ docker build -t ipeacocks/watch-price-checker .

$ docker run -d \
    -e FROMADDR="address@gmail.com" \
    -e TOADDR="address@gmail.com" \
    -e EMAIL_PASS="p@ssw0rd" \
    -e DISPLAY=:55 \
    -it ipeacocks/watch-price-checker
```
Script downloads [Jomashop page](https://www.jomashop.com/watches-for-men.html?manufacturer=Junghans&series=Max+Bill%7CMax+Bill+Mega&sort=price_asc%7Casc) with Selenium/Firefox in Xvfb session and then parses it with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and sends email when there will be watch which costs less than `$PRICE_LIMIT`.