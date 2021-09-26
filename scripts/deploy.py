from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import deploy_mock, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3

def deploy_fund_me() :
    account = get_account()

    # Pass the price feed address to out fundme constructor
    if network.show_active() not in  LOCAL_BLOCKCHAIN_ENVIRONMENTS :
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else :
        deploy_mock()
        price_feed_address = MockV3Aggregator[-1].address
        
    fundme = FundMe.deploy(price_feed_address, {
        "from" : account
    }, publish_source = config["networks"][network.show_active()].get("verify"))
    print(f"Contract deployed to {fundme.address}")
    return fundme

def main() :
    deploy_fund_me()