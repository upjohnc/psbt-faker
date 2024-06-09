from base64 import b64encode
from binascii import b2a_hex as _b2a_hex
from decimal import Decimal

import click

from psbt_faker.txn import ADDR_STYLES, fake_txn

b2a_hex = lambda a: str(_b2a_hex(a), "ascii")

SIM_XPUB = "tpubD6NzVbkrYhZ4XzL5Dhayo67Gorv1YMS7j8pRUvVMd5odC2LBPLAygka9p7748JtSq82FNGPppFEz5xxZUdasBRCqJqXvUHq6xpnsMcYJzeh"


@click.command()
@click.argument("out_psbt", type=click.File("wb"), metavar="OUTPUT.PSBT")
@click.argument("xpub", type=str, default=SIM_XPUB)
@click.option("--num-outs", "-n", help="Number of outputs (default 1)", default=1)
@click.option(
    "--num-change", "-c", help="Number of change outputs (default 1)", default=1
)
@click.option(
    "--value", "-v", help="Total BTC value of inputs (integer, default 3)", default=3
)
@click.option("--fee", "-f", help="Miner's fee in Satoshis", default=1000)
@click.option(
    "--segwit", "-s", help="Make ins/outs be segwit style", is_flag=True, default=False
)
@click.option(
    "--styles",
    "-a",
    help="Output address style (multiple ok)",
    multiple=True,
    default=None,
    type=click.Choice(ADDR_STYLES),
)
@click.option(
    "--base64", "-6", help="Output base64 (default binary)", is_flag=True, default=False
)
@click.option(
    "--testnet",
    "-t",
    help="Assume testnet3 addresses (default mainnet)",
    is_flag=True,
    default=False,
)
@click.option(
    "--partial",
    "-p",
    help="Change first input so its different XPUB and result cannot be finalized",
    is_flag=True,
    default=False,
)
@click.option(
    "--zero-xfp",
    "-z",
    help="Provide zero XFP and junk XPUB (cannot be signed, but should be decodable)",
    is_flag=True,
    default=False,
)
def faker(
    num_change,
    num_outs,
    out_psbt,
    value,
    testnet,
    xpub,
    segwit,
    fee,
    styles,
    base64,
    partial,
    zero_xfp,
):
    """Construct a valid PSBT which spends non-existent BTC to random addresses!"""

    num_ins = int(value)
    total_outs = num_outs + num_change

    if zero_xfp:
        xpub = None

    chg_style = "p2pkh" if not segwit else "p2wpkh"

    if not styles:
        styles = [chg_style]

    psbt, outs = fake_txn(
        num_ins,
        total_outs,
        master_xpub=xpub,
        fee=fee,
        segwit_in=segwit,
        outstyles=styles,
        change_style=chg_style,
        partial=partial,
        is_testnet=testnet,
        change_outputs=list(range(num_outs, num_outs + num_change)),
    )

    out_psbt.write(psbt if not base64 else b64encode(psbt))

    print(f"\nFake PSBT would send {num_ins} BTC to: ")
    print(
        "\n".join(
            " %.8f => %s %s" % (amt, dest, " (change back)" if chg else "")
            for amt, dest, chg in outs
        )
    )
    if fee:
        print(" %.8f => miners fee" % (Decimal(fee) / Decimal(1e8)))

    print("\nPSBT to be signed: " + out_psbt.name, end="\n\n")


if __name__ == "__main__":
    # main()
    faker()
