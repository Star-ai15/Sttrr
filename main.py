
import os, base64, asyncio
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from solana.publickey import PublicKey
from spl.token.async_client import AsyncToken

RPC = "https://api.mainnet-beta.solana.com"
STAR = PublicKey("7Hajt3Yc7MQhWwNsUAxdUgcLH7M59u1bDpZ79E5Zkmat")
SECRET = base64.b64decode(os.environ["PRESALE_SECRET"])
KP = Keypair.from_secret_key(SECRET)
WALLET = KP.public_key
RATIO = 300_000_000 / 700

async def run():
    client = AsyncClient(RPC)
    token = AsyncToken(client, STAR, PublicKey("Tokenkeg...DA"), KP)
    seen = set()
    while True:
        sigs = (await client.get_signatures_for_address(WALLET, limit=10)).value
        for s in sigs:
            if s.signature in seen: continue
            tx = await client.get_transaction(s.signature)
            if not tx: continue
            sender = tx.transaction.message.account_keys[0]
            sol = (tx.meta.post_balances[0] - tx.meta.pre_balances[0]) / 1e9
            if sol <= 0: continue
            amt = int(sol * RATIO * 1_000_000)
            await token.transfer(WALLET, sender, WALLET, amt, 6)
            seen.add(s.signature)
            print("Sent", amt, "STAR to", sender)
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(run())
