
import os, base64, asyncio
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from solana.keypair import Keypair

RPC = "https://api.mainnet-beta.solana.com"
OPAL_WALLET = PublicKey("FNVruuziVqeYor5xNkx2ENsndjonqiWLEMjnXUs7JuXe")

async def monitor_opal():
    client = AsyncClient(RPC)
    print("Watching for Opal purchases...")
    seen = set()
    while True:
        sigs = (await client.get_signatures_for_address(OPAL_WALLET, limit=20)).value
        for sig in sigs:
            if sig.signature in seen: continue
            tx = await client.get_transaction(sig.signature)
            post_bal = tx.meta.post_balances[0]
            pre_bal = tx.meta.pre_balances[0]
            sol_amount = (post_bal - pre_bal) / 1e9
            buyer = tx.transaction.message.account_keys[0]
            if sol_amount >= 0.03 and sol_amount < 0.045:
                print("Small Opal purchase from", buyer, f"{sol_amount:.2f} SOL")
            elif sol_amount >= 0.06:
                print("Large Opal purchase from", buyer, f"{sol_amount:.2f} SOL")
            seen.add(sig.signature)
        await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(monitor_opal())
