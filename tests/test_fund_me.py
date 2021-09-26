from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

def test_can_fund_and_withdraw() :
    account = get_account()
    fund_me = deploy_fund_me()
    print(f"Address {fund_me.address}")
    entrance_fee = fund_me.getEntranceFee() + 100
    print(f"The entrance_fee is {entrance_fee}")
    transaction1 = fund_me.fund({
        "from" : account,
        "value" : entrance_fee
    })
    transaction1.wait(1)
    assert fund_me.addressToAmountFund(account.address) == entrance_fee
    transaction2 = fund_me.withdraw({
        "from" : account
    })
    transaction2.wait(1)
    assert fund_me.addressToAmountFund(account.address) == 0


def test_only_owner_can_withdraw() :
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS :
        pytest.skip("Only for local testnet")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError) :
        fund_me.withdraw({
            "from" : bad_actor
        })