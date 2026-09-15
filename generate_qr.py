import qrcode

base_url = " https://spearfish-fresh-electable.ngrok-free.dev"  # ← ton URL ngrok

for path in ["qr1", "qr2", "response"]:
    img = qrcode.make(f"{base_url}/{path}")
    img.save(f"qr_{path}.png")