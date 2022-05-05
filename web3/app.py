from pywebio import *
from pywebio.output import *
from pywebio.input import *
import charts
from web3 import Web3
from web3.exceptions import BlockNotFound, TransactionNotFound
import os


def put_account_search(web3, account_search):
    popup("Account Info", [put_scope("popup_content")], PopupSize.LARGE)
    with use_scope("popup_content"):
        if web3.isAddress(account_search):
            balance = web3.eth.get_balance(account_search)
            transaction_count = web3.eth.get_transaction_count(account_search)
            put_table(
                tdata=[
                    ["Balance", f"{web3.fromWei(balance, 'ether'):,.0f} ether"],
                    ["Transaction Count", transaction_count],
                ],
                header=[f"Info on {account_search}", None],
            )
        else:
            put_markdown(f"**Account not found**").style("color: red")


@use_scope("dashboard", clear=True)
def put_blocks(web3):
    put_markdown("## Blocks")
    put_scope("search")
    put_scope("results")
    put_scope("latest")
    with use_scope("search"):
        put_row(
            [
                pin.put_input(
                    type=NUMBER,
                    name="block_search",
                    placeholder="Enter block number to lookup",
                ),
                None,
                put_button(
                    "Search",
                    onclick=lambda: put_block_search(web3, pin.pin["block_search"]),
                    outline=True,
                ),
            ],
            size="40% 10px 15%",
        )
    # * Latest blocks
    put_latest_blocks(web3)


@use_scope("results", clear=True)
def put_block_search(web3, block_number):
    if block_number != None:
        try:
            this_block = web3.eth.get_block(block_number)
            with use_scope("results", clear=True):
                put_markdown(f"### Block #{this_block['number']}")
                put_table(
                    tdata=[
                        ["Hash", this_block["hash"].hex()],
                        ["Difficulty", this_block["difficulty"]],
                        ["Gas Used", this_block["gasUsed"]],
                        [
                            "Miner",
                            put_button(
                                this_block["miner"],
                                onclick=lambda: put_account_search(
                                    web3, this_block["miner"]
                                ),
                                link_style=True,
                            ),
                        ],
                    ],
                    header=["Properties", "Values"],
                )
        except BlockNotFound:
            print("Not found")


@use_scope("latest")
def put_latest_blocks(web3):
    latest_block = web3.eth.get_block("latest")["number"]
    blocks = []
    for i in range(10):
        block = web3.eth.get_block(latest_block - i)
        blocks.append(
            [
                put_button(
                    block["number"],
                    onclick=lambda x=block["number"]: put_block_search(web3, x),
                    link_style=True,
                ),
                block["difficulty"],
                put_button(
                    block["miner"],
                    onclick=lambda x=block["miner"]: put_account_search(web3, x),
                    link_style=True,
                ),
            ]
        )
    put_markdown("### Latest Blocks")
    put_table(tdata=blocks, header=["Block", "Difficulty", "Miner"])


@use_scope("dashboard", clear=True)
def put_transactions(web3):
    put_markdown("## Transactions")
    put_scope("search")
    put_scope("results")
    put_scope("latest")
    with use_scope("search"):
        put_row(
            [
                pin.put_input(
                    type=TEXT,
                    name="transaction_search",
                    placeholder="Enter transaction hash to lookup",
                ),
                None,
                put_button(
                    "Search",
                    onclick=lambda: put_transaction_search(
                        web3, pin.pin["transaction_search"]
                    ),
                    outline=True,
                ),
            ],
            size="40% 10px 15%",
        )
    put_latest_transactions(web3)


@use_scope("results")
def put_transaction_search(web3, transaction_hash):
    if transaction_hash != None:
        try:
            this_tx = web3.eth.get_transaction(transaction_hash)
            with use_scope("results", clear=True):
                put_markdown(f"### Transaction {this_tx['blockHash'].hex()}")
                put_table(
                    tdata=[
                        ["Hash", this_tx["hash"].hex()],
                        [
                            "From",
                            put_button(
                                this_tx["from"],
                                onclick=lambda: put_account_search(
                                    web3, this_tx["from"]
                                ),
                                link_style=True,
                            ),
                        ],
                        [
                            "To",
                            put_button(
                                this_tx["to"],
                                onclick=lambda: put_account_search(web3, this_tx["to"]),
                                link_style=True,
                            ),
                        ],
                        [
                            "Value",
                            f"{web3.fromWei(this_tx['value'], 'ether'):,.2f} ether",
                        ],
                        ["Gas", this_tx["gas"]],
                    ],
                    header=["Properties", "Values"],
                )
        except TransactionNotFound:
            put_markdown("#### Transaction Not found").style("color: red")


@use_scope("latest")
def put_latest_transactions(web3):
    latest_transactions = []
    latest_block = web3.eth.get_block("latest")
    for tx_hash in latest_block["transactions"][-10:]:
        tx = web3.eth.get_transaction(tx_hash)
        latest_transactions.append(
            [
                put_button(
                    f"{tx['hash'].hex()[0:10]}...",
                    onclick=lambda x=tx["hash"].hex(): put_transaction_search(web3, x),
                    link_style=True,
                ),
                put_button(
                    f"{tx['from'][0:10]}...",
                    onclick=lambda x=tx["from"]: put_account_search(web3, x),
                    link_style=True,
                ),
                put_button(
                    f"{tx['to'][0:10]}...",
                    onclick=lambda x=tx["to"]: put_account_search(web3, x),
                    link_style=True,
                ),
                f"{web3.fromWei(tx['value'], 'ether'):,.2f} ether",
            ]
        )
    put_table(
        tdata=latest_transactions, header=["Recent Transactions", "From", "To", "Value"]
    )


@use_scope("left_navbar")
def put_navbar(web3):
    put_grid(
        [
            [
                put_markdown("### PyWebIO Ether Demo"),
                put_markdown("#### Charts").onclick(lambda: put_charts(web3)),
                put_markdown("#### Blocks").onclick(lambda: put_blocks(web3)),
                put_markdown("#### Transactions").onclick(
                    lambda: put_transactions(web3)
                ),
            ]
        ],
        direction="column",
    )


@use_scope("dashboard", clear=True)
def put_charts(web3):
    put_markdown("## Charts")
    put_html(charts.get_block_miners(web3)).style("width: 60vw; height: 40rem")
    put_markdown(
        "###### This graph shows the miners who mined the most blocks from a sample of 1,000 blocks."
    )
    put_markdown("---")


@config(theme="dark")
def main():
    session.set_env(title="PyWebIO Ethereum Demo", output_max_width="100%")
    # config(title="PyWebIO Ethereum Demo", theme="dark")
    if "INFURA_URL" in os.environ:
        url = os.environ["INFURA_URL"].  ## 
        web3 = Web3(Web3.HTTPProvider(url))
        # Setup layout
        put_row(
            [put_scope("left_navbar"), None, put_scope("dashboard")],
            size="1fr 50px 4fr",
        )
        put_navbar(web3)
        put_charts(web3)

    else:
        put_markdown("## Error: No Infura URL Setup")


if __name__ == "__main__":
    start_server(port=8080, applications=main)
