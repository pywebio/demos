import plotly.express as px
import pickle
from app import _web3
import os

chart_data_file = os.path.join(os.path.dirname(__file__), "__chart_data.ob")

#At first run, download data for the latest blocks and save to a local pickle file
def generate_data(n=1000):
    latest_block_num = _web3.eth.get_block("latest")["number"]
    blocks = []
    for i in range(n):
        blocks.append(_web3.eth.get_block(latest_block_num - i))
    miners = {}
    for block in blocks:
        block_miner = block["miner"]
        if block_miner in miners:
            miners[block_miner] += 1
        else:
            miners[block_miner] = 1
    sorted_data = {
        k: v for k, v in sorted(miners.items(), key=lambda item: item[1], reverse=True)
    }
    with open(chart_data_file, "wb") as fp:
        pickle.dump(sorted_data, fp)
    return sorted_data


def get_block_miners():
    data = get_data()
    fig = px.line(
        x=range(len(data.values())),
        y=data.values(),
        labels={"x": "Miner Rank", "y": "Number of Blocks Mined"},
        title=f"Top Mining Accounts from Sample of 1,000 Blocks",
        template="plotly_dark",
    )
    return fig.to_html(include_plotlyjs="require", full_html=False)


def get_data():
    global chart_data_file
    try:
        with open(chart_data_file, "rb") as fp:
            try:
                data = pickle.load(fp)
            except EOFError:
                data = generate_data()
    except:
        data = generate_data()
    return data
