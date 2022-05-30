from amadeus import Client, ResponseError

amadeus = Client(
    client_id='qnizwdeLBSiY0xBOndcC9EbOW79NzNE6',
    client_secret='MqmuJJmRlEljItZw'
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='MAD',
        destinationLocationCode='ATH',
        departureDate='2022-11-01',
        adults=1)
    print(response.data)
except ResponseError as error:
    print(error)