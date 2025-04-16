from tronpy import Tron
from tronpy.exceptions import AddressNotFound

client = Tron()

def get_tron_info(address: str) -> dict:
    try:
        balance = client.get_account_balance(address)
        resource = client.get_account_resource(address)

        free_net_remaining = resource.get("freeNetLimit", 0) - resource.get("freeNetUsed", 0)
        net_remaining = resource.get("NetLimit", 0) - resource.get("NetUsed", 0)
        bandwidth = free_net_remaining + net_remaining

        energy = resource.get("EnergyLimit", 0) - resource.get("EnergyUsed", 0)
    except AddressNotFound:
        raise Exception("Кошелек не найден")
    except Exception as e:
        raise Exception(f"Ошибка API Tron: {e}")

    return {
        "balance_trx": balance,
        "bandwidth": bandwidth,
        "energy": energy
    }
