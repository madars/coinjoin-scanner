#!/usr/bin/env python3
from bitcoin.core import CBlock, CTransaction # bitcoinlib
from pathlib import Path
import pbk # pybitcoinkernel

datadir = Path("/scratch/madars/bitcoin")
start_height = 572030

whirlpool_genesis_txns = [
    "c6c27bef217583cca5f89de86e0cd7d8b546844f800da91d91a74039c3b40fba",
    "94b0da89431d8bd74f1134d8152ed1c7c4f83375e63bc79f19cf293800a83f52",
    "b42df707a3d876b24a22b0199e18dc39aba2eafa6dbeaaf9dd23d925bb379c59",
    "4c906f897467c7ed8690576edfcaf8b1fb516d154ef6506a2c4cab2c48821728",
    "a42596825352055841949a8270eda6fb37566a8780b2aec6b49d8035955d060e",
    "a554db794560458c102bab0af99773883df13bc66ad287c29610ad9bac138926",
    "792c0bfde7f6bf023ff239660fb876315826a0a52fd32e78ea732057789b2be0"
]

####

def is_whirlpool(tx, prev_whirlpools):
    """Check if a transaction is a WhirlPool tx. It is caller's
    responsibility to update prev_whirlpools if so.

    Translated from https://github.com/ishaanam/bitcoin/blob/coinjoin_detection/src/util/coinjoins.cpp#L7"""
    if len(tx.vin) != 5 or len(tx.vout) != 5:
        return False

    common_amount = tx.vout[0].nValue
    if common_amount not in [5000000, 1000000, 50000000]:
        return False

    if any(vout.nValue != common_amount for vout in tx.vout):
        return False
    
    if all(vin.prevout.hash[::-1].hex() not in prev_whirlpools for vin in tx.vin):
        return False

    return True

def process(chainman):
    end_height = chainman.get_block_index_from_tip().height

    whirlpool_txids = whirlpool_genesis_txns
    for block_index in pbk.block_index_generator(chainman, start_height, end_height):
        if block_index.height % 100 == 0:
            print("still processing ... height =", block_index.height)
        block_data = chainman.read_block_from_disk(block_index)

        cblock = CBlock.deserialize(block_data.data)
        for tx in cblock.vtx:
            if is_whirlpool(tx, whirlpool_txids):
                print(tx.GetHash()[::-1].hex())
                whirlpool_txids += [tx.GetHash()[::-1].hex()]

def init_chainman():
    chainman = pbk.load_chainman(datadir, pbk.ChainType.MAINNET)
    return chainman
    
if __name__ == '__main__':
    """We split out the expensive initialization into a separate
    function, so that we can do the following from iPython:

    %load_ext autoreload
    %autoreload 2
    from coinjoin_scanner import *
    chainman = init_chainman()
    process(chainman)

    # ... edit your code

    process(chainman)
    """
    chainman = init_chainman()
    process(chainman)
