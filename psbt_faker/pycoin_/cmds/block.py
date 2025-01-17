#!/usr/bin/env python

import argparse
import datetime

from pycoin_.block import Block
from pycoin_.cmds.tx import dump_tx
from pycoin_.networks.default import get_current_netcode
from pycoin_.serialize import b2h, b2h_rev, stream_to_bytes


def dump_block(block, netcode=None):
    if netcode is None:
        netcode = get_current_netcode()
    blob = stream_to_bytes(block.stream)
    print("%d bytes   block hash %s" % (len(blob), block.id()))
    print("version %d" % block.version)
    print("prior block hash %s" % b2h_rev(block.previous_block_hash))
    print("merkle root %s" % b2h(block.merkle_root))
    print("timestamp %s" % datetime.datetime.utcfromtimestamp(block.timestamp).isoformat())
    print("difficulty %d" % block.difficulty)
    print("nonce %s" % block.nonce)
    print("%d transaction%s" % (len(block.txs), "s" if len(block.txs) != 1 else ""))
    for idx, tx in enumerate(block.txs):
        print("Tx #%d:" % idx)
        dump_tx(tx, netcode=netcode, verbose_signature=False, disassembly_level=0, do_trace=False, use_pdb=False)


def create_parser():
    parser = argparse.ArgumentParser(description="Dump a block in human-readable form.")
    parser.add_argument("block_file", nargs="+", type=argparse.FileType('rb'),
                        help='The file containing the binary block.')
    return parser


def block(args, parser):
    for f in args.block_file:
        block = Block.parse(f)
        dump_block(block)
        print('')


def main():
    parser = create_parser()
    args = parser.parse_args()
    block(args, parser)


if __name__ == '__main__':
    main()
