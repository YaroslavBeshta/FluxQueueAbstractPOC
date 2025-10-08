import lxml.html


def process_yahoo_response(response) -> float:
    tree = lxml.html.fromstring(response.text)
    market_price = tree.xpath(
        '//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]'
    )[0].text
    market_price = float(market_price.replace(",", ""))
    return market_price
