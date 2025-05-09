from typing import Dict, Optional

# Common coin symbol to CoinGecko ID mapping
SYMBOL_TO_ID_MAPPING: Dict[str, str] = {
    # Major cryptocurrencies
    "btc": "bitcoin",
    "eth": "ethereum",
    "usdt": "tether",
    "bnb": "binancecoin",
    "xrp": "ripple",
    "ada": "cardano",
    "doge": "dogecoin",
    "sol": "solana",
    "dot": "polkadot",
    "shib": "shiba-inu",
    "ltc": "litecoin",
    "link": "chainlink",
    "avax": "avalanche-2",
    "matic": "matic-network",
    "trx": "tron",
    "etc": "ethereum-classic",
    "xlm": "stellar",
    "near": "near",
    "algo": "algorand",
    "atom": "cosmos",
    
    # Stablecoins
    "usdc": "usd-coin",
    "dai": "dai",
    "busd": "binance-usd",
    "tusd": "true-usd",
    "usdd": "usdd",
    "gusd": "gemini-dollar",
    "pax": "paxos-standard",
    "lusd": "liquity-usd",
    "frax": "frax",
    "cusd": "celo-dollar",
    
    # DeFi tokens
    "uni": "uniswap",
    "aave": "aave",
    "cake": "pancakeswap-token",
    "crv": "curve-dao-token",
    "sushi": "sushi",
    "comp": "compound-governance-token",
    "mkr": "maker",
    "snx": "synthetix-network-token",
    "bal": "balancer",
    "yfi": "yearn-finance",
    
    # Others
    "mana": "decentraland",
    "sand": "the-sandbox",
    "grt": "the-graph",
    "axs": "axie-infinity",
    "ftm": "fantom",
    "hbar": "hedera-hashgraph",
    "theta": "theta-token",
    "xtz": "tezos",
    "vet": "vechain",
    "egld": "elrond-erd-2",
    "icp": "internet-computer",
    "fil": "filecoin",
    "xmr": "monero",
    "eos": "eos",
    "bch": "bitcoin-cash",
    "flow": "flow",
    "kcs": "kucoin-shares",
    "neo": "neo",
    "one": "harmony",
    "qtum": "qtum",
    "zec": "zcash",
    "dash": "dash",
    "lunc": "terra-luna",
    "usdp": "paxos-standard",
    "celo": "celo",
    "stx": "blockstack",
    "bat": "basic-attention-token"
}

def get_coin_id(input_text: str) -> str:
    """
    Maps a coin symbol or name to its CoinGecko ID.
    
    Args:
        input_text: The user input text (symbol or name)
        
    Returns:
        The CoinGecko coin ID or the original input if no mapping is found
    """
    # Convert to lowercase for case-insensitive matching
    input_text = input_text.lower()
    
    # If it's already in the mapping, return the ID
    if input_text in SYMBOL_TO_ID_MAPPING:
        return SYMBOL_TO_ID_MAPPING[input_text]
    
    # Otherwise return the original (might be a full name like "bitcoin")
    return input_text

def get_symbol_from_id(coin_id: str) -> Optional[str]:
    """
    Get the symbol for a given coin ID.
    
    Args:
        coin_id: The CoinGecko coin ID
        
    Returns:
        The symbol in uppercase if found, None otherwise
    """
    for symbol, id_value in SYMBOL_TO_ID_MAPPING.items():
        if id_value == coin_id.lower():
            return symbol.upper()
    return None

def is_stablecoin(coin_id_or_symbol: str) -> bool:
    """
    Check if a coin is a stablecoin based on its ID or symbol.
    
    Args:
        coin_id_or_symbol: The coin ID or symbol
        
    Returns:
        True if it's a stablecoin, False otherwise
    """
    # Check if it's a symbol first and convert to ID if needed
    coin_id = get_coin_id(coin_id_or_symbol)
    
    stablecoins = [
        "tether", "usd-coin", "binance-usd", "dai", "true-usd", 
        "usdd", "frax", "paxos-standard", "gemini-dollar", "liquity-usd",
        "celo-dollar", "neutrino", "fei-usd", "origin-dollar"
    ]
    
    return coin_id in stablecoins