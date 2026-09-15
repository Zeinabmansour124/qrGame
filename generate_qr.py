import qrcode

BASE_URL = "https://abc-def-123.trycloudflare.com"

qrcode.make(BASE_URL + "/qr1").save("QR1.png")
qrcode.make(BASE_URL + "/qr2").save("QR2.png")

print("QR1.png et QR2.png créés.")