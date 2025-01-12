Release History
==============

### Version 2.10.1
Released on Dec 22, 2020

#### Update
* Upgrade dependencies so that this SDK can run on Apple M1 Chip.

### Version 2.10.1-beta0
Released on Dec 22, 2020

#### Update
* Upgrade dependencies so that this SDK can run on Apple M1 Chip.

### Version 2.10.0

Released on Nov 15, 2020

**This update include breaking changes**

#### Breaking changes
* feat: check the mnemonic is correct before using it to generate the seed. ([#406](https://github.com/StellarCN/py-stellar-base/pull/406))
    - A parameter named `language` is added to `stellar_sdk.keypair.Keypair.from_mnemonic_phrase()`.

### Version 2.9.0

Released on Nov 11, 2020

**This update include breaking changes**

#### Breaking changes
* Updates the SEP-10 utility function parameters and return values to support [SEP-10 v3.0](https://github.com/stellar/stellar-protocol/commit/9d121f98fd2201a5edfe0ed2befe92f4bf88bfe4) ([#400](https://github.com/StellarCN/py-stellar-base/pull/400))

    - The following functions replaced the `domain_name` parameter with `home_domains`:

        - `stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold()`
        - `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction()`

    - The following function replaced the `domain_name` parameter with `home_domain`:
        - `stellar_sdk.sep.stellar_web_authentication.build_challenge_transaction()`

    - `stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction()` now returns an additional object attribute, `matched_home_domain`


### Version 2.8.1

Released on Oct 15, 2020

#### Update
* feat: add support for SEP-0010 v2.1.0. ([#380](https://github.com/StellarCN/py-stellar-base/pull/380))

In SEP-10 SEP-0010 v2.1.0, the `domain_name` field is no longer needed, but we still keep it to reduce breaking changes.


### Version 2.8.0

Released on Oct 04, 2020

**This update include breaking changes**

#### Update

* feat: add support for Stellar Protocol 14. ([#367](https://github.com/StellarCN/py-stellar-base/pull/367))

#### Added

- feat: add support for [CAP-23](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0023.md). ([#371](https://github.com/StellarCN/py-stellar-base/pull/371))

  We have added methods to `TransactionBuilder`, you can use them to construct corresponding operations, method list:

  - append_create_claimable_balance_op
  - append_claim_claimable_balance_op

  We have added `ClaimPredicate`, please use helper function to build ClaimPredicate, method list:

  - predicate_and
  - predicate_or
  - predicate_not
  - predicate_before_absolute_time
  - predicate_before_relative_time
  - predicate_unconditional

  The following is an [example](https://github.com/StellarCN/py-stellar-base/blob/9a6f1e4a3dbf2693016e678b108737b3a7cfb967/examples/claimable_balances.py).

  ```python
  from stellar_sdk import Server, TransactionBuilder, Keypair, ClaimPredicate, Claimant, Asset, Network
  
  sponsor_secret = "SAOJHTVFCYVKUMPNQI7RUSI566GKWXP7RXOHP4SV6JAVUQKSIWGPZFPJ"
  claimant_secret = "SBOLGU7D7A7MTY4JZ3WZUKSKB6NZBQFNQG3BZT4HZW4AAVZJRG7TWXGQ"
  
  sponsor_keypair = Keypair.from_secret(sponsor_secret)
  claimant_keypair = Keypair.from_secret(claimant_secret)
  
  server = Server("https://horizon-testnet.stellar.org")
  network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
  
  # Create Claimable Balance
  sponsor_account = server.load_account(sponsor_keypair.public_key)
  
  predicate_left = ClaimPredicate.predicate_before_relative_time(60 * 60 * 24 * 7)
  predicate_right = ClaimPredicate.predicate_not(ClaimPredicate.predicate_before_relative_time(60 * 3))
  predicate = ClaimPredicate.predicate_and(predicate_left, predicate_right)
  claimant = Claimant(destination=claimant_keypair.public_key, predicate=predicate)
  create_claimable_balance_te = TransactionBuilder(
      source_account=sponsor_account,
      network_passphrase=network_passphrase
  ).append_create_claimable_balance_op(
      asset=Asset.native(),
      amount="100",
      claimants=[claimant],
      source=sponsor_keypair.public_key
  ).build()
  create_claimable_balance_te.sign(sponsor_keypair)
  create_claimable_balance_resp = server.submit_transaction(create_claimable_balance_te)
  print(create_claimable_balance_resp)
  
  # Claim Claimable Balance
  balance_id = "00000000550e14acbdafcd3089289363b3b0c8bec9b4edd87298c690655b4b2456d68ba0"
  claimant_account = server.load_account(claimant_keypair.public_key)
  claim_claimable_balance_te = TransactionBuilder(
      source_account=claimant_account,
      network_passphrase=network_passphrase
  ).append_claim_claimable_balance_op(
      balance_id=balance_id,
      source=claimant_keypair.public_key
  ).build()
  
  claim_claimable_balance_te.sign(claimant_keypair)
  claim_claimable_balance_resp = server.submit_transaction(claim_claimable_balance_te)
  print(claim_claimable_balance_resp)
  ```

- feat: add support for [CAP-33](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0033.md). ([#372](https://github.com/StellarCN/py-stellar-base/pull/372) [#374](https://github.com/StellarCN/py-stellar-base/pull/374))

  We have added methods to `TransactionBuilder`, you can use them to construct corresponding operations, method list:

  - append_begin_sponsoring_future_reserves_op
  - append_end_sponsoring_future_reserves_op
  - append_revoke_account_sponsorship_op
  - append_revoke_trustline_sponsorship_op
  - append_revoke_offer_sponsorship_op
  - append_revoke_data_sponsorship_op
  - append_revoke_claimable_balance_sponsorship_op
  - append_revoke_ed25519_public_key_signer_sponsorship_op
  - append_revoke_hashx_signer_sponsorship_op
  - append_revoke_pre_auth_tx_signer_sponsorship_op

  The following is an [example](https://github.com/StellarCN/py-stellar-base/blob/9a6f1e4a3dbf2693016e678b108737b3a7cfb967/examples/sponsored_reserves.py).

  ```python
  from stellar_sdk import Server, TransactionBuilder, Keypair, Network
  
  sponsor_secret = "SAOJHTVFCYVKUMPNQI7RUSI566GKWXP7RXOHP4SV6JAVUQKSIWGPZFPJ"
  new_account_secret = "SCN5D72JHQAHUHGIA23SLS3LBYCPHJWD7HLYNJRBBZIG4PD74UCGQBYM"
  
  sponsor_keypair = Keypair.from_secret(sponsor_secret)
  newly_created_keypair = Keypair.from_secret(new_account_secret)
  
  server = Server("https://horizon-testnet.stellar.org")
  network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
  
  # Sponsoring Account Creation
  # https://github.com/stellar/stellar-protocol/blob/master/core/cap-0033.md#example-sponsoring-account-creation
  sponsor_account = server.load_account(sponsor_keypair.public_key)
  sponsoring_account_creation_te = TransactionBuilder(
      source_account=sponsor_account,
      network_passphrase=network_passphrase
  ).append_begin_sponsoring_future_reserves_op(
      sponsored_id=newly_created_keypair.public_key,
      source=sponsor_keypair.public_key
  ).append_create_account_op(
      destination=newly_created_keypair.public_key,
      starting_balance="10",
      source=sponsor_keypair.public_key
  ).append_end_sponsoring_future_reserves_op(
      source=newly_created_keypair.public_key
  ).build()
  sponsoring_account_creation_te.sign(sponsor_keypair)
  sponsoring_account_creation_te.sign(new_account_secret)
  sponsoring_account_creation_resp = server.submit_transaction(sponsoring_account_creation_te)
  print(sponsoring_account_creation_resp)
  
  # Revoke Account Sponsorship
  sponsor_account = server.load_account(sponsor_keypair.public_key)
  revoke_account_sponsorship_te = TransactionBuilder(
      source_account=sponsor_account,
      network_passphrase=network_passphrase
  ).append_revoke_account_sponsorship_op(
      account_id=newly_created_keypair.public_key,
      source=sponsor_keypair.public_key
  ).build()
  revoke_account_sponsorship_te.sign(sponsor_keypair)
  revoke_account_sponsorship_resp = server.submit_transaction(revoke_account_sponsorship_te)
  print(revoke_account_sponsorship_resp)
  ```

- feat: add support for new endpoint of Protocol 14. ([#373](https://github.com/StellarCN/py-stellar-base/pull/373))

  The following are the newly added endpoints.

  - server.claimable_balances().claimable_balance(claimable_balance_id)
  - server.claimable_balances().for_asset(asset)
  - server.claimable_balances().for_sponsor(sponsor)
  - server.claimable_balances().for_claimant(claimant)
  - server.accounts().for_sponsor(sponsor)
  - server.offers().for_sponsor(sponsor)

#### Breaking changes

* The type of `stellar_sdk.signer.Signer.signer_key` is changed from  `Xdr.types.SignerKey` to  `stellar_sdk.signer_key.SignerKey`.

### Version 2.7.0

Released on Aug 28, 2020

**This update include breaking changes**

#### Update
* feat: add support for SEP-0010 v2.0.0. ([#363](https://github.com/StellarCN/py-stellar-base/pull/363))

#### Breaking changes

Due to the addition of support for SEP-10 v2.0.0, we no longer support SEP-10 v1.x. 

The **domain_name** parameter is required in SEP-10, and the **anchor_name** parameter is no longer needed, you can get these SEP-10 changes [here](https://github.com/stellar/stellar-protocol/pull/708).

There have been some breaking changes to SEP-10 related functions, the following is a breaking changes list, you can also check our [latest document](https://stellar-sdk.readthedocs.io/en/2.7.0/api.html#sep-0010-stellar-web-authentication).

- stellar_sdk.sep.stellar_web_authentication.build_challenge_transaction (**domain_name** parameter is required, **anchor_name**  parameter has been removed.)
- stellar_sdk.sep.stellar_web_authentication.read_challenge_transaction (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signers (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_threshold (**domain_name** parameter is required)
- stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction (**domain_name** parameter is required)


### Version 2.6.4

Released on Aug 14, 2020

#### Added
* feat: add support for parsing Stellar URI (SEP-0007). ([#360](https://github.com/StellarCN/py-stellar-base/pull/360))

### Version 2.6.3

Released on Aug 09, 2020

#### Added
* feat: add support to SEP-0011 (Txrep: human-readable low-level representation of Stellar transactions). ([#357](https://github.com/StellarCN/py-stellar-base/pull/357))

### Version 2.6.2

Released on Jul 20, 2020

#### Added
* feat: add support for SEP-0007 (URI Scheme to facilitate delegated signing). ([#349](https://github.com/StellarCN/py-stellar-base/pull/349))

### Version 2.6.1

Released on Jun 21, 2020

**This update has breaking changes compared to 2.5.3.**

For [some reason](https://github.com/StellarCN/py-stellar-base/issues/338), we yanked [2.6.0](https://pypi.org/project/stellar-sdk/2.6.0/) on PyPi, 
but actually 2.6.0 can be used normally. 

This update log will contain the updated content of 2.6.0.

#### Update
- Optimize SEP-10, when you call `stellar_sdk.sep.stellar_web_authentication.verify_challenge_transaction_signed_by_client_master_key`, 
  an exception will be thrown if the transaction contains extra signatures. ([#338](https://github.com/StellarCN/py-stellar-base/pull/338)) (2.6.1)
- Generate V1 transactions by default. ([#337](https://github.com/StellarCN/py-stellar-base/pull/337)) (2.6.0)
- Allow V0 transactions to be fee bumped. ([#331](https://github.com/StellarCN/py-stellar-base/pull/331)) (2.6.0)

#### Breaking changes
- The default values of the following parameters have changed, 
  they used to default to False, but now they default to True. (2.6.0)
    - the `v1` parameter in stellar_sdk.transaction_builder.TransactionBuilder
    - the `v1` parameter in stellar_sdk.transaction.Transaction
    
### Version 2.6.0

Released on Jun 18, 2020

**This update include breaking changes**

#### Update
- Generate V1 transactions by default. ([#337](https://github.com/StellarCN/py-stellar-base/pull/337))
- Allow V0 transactions to be fee bumped. ([#331](https://github.com/StellarCN/py-stellar-base/pull/331))

#### Breaking changes
- The default values of the following parameters have changed, 
  they used to default to False, but now they default to True.
    - the `v1` parameter in stellar_sdk.transaction_builder.TransactionBuilder
    - the `v1` parameter in stellar_sdk.transaction.Transaction

### Version 2.5.3

Released on Jun 14, 2020

#### Fixed
- Set the value of the `v1` property correctly when calling TransactionBuilder.from_xdr. ([#333](https://github.com/StellarCN/py-stellar-base/pull/333))


### Version 2.5.2

Released on Jun 03, 2020

#### Update
- Optimized the way to read xdr. In 2.5.x, we will discard the id in muxed account, 
    in this update, we will keep the id, but it is invisible to users. 
    We recommend that all users using 2.5.x upgrade to this version. ([#326](https://github.com/StellarCN/py-stellar-base/pull/326))
  
### Version 2.5.1

Released on May 27, 2020

#### Added

- add `stellar_sdk.call_builder.PaymentsCallBuilder.join` ([#323](https://github.com/StellarCN/py-stellar-base/pull/323))

  ```python
  from stellar_sdk import Server
  
  horizon_url = "https://horizon.stellar.org/"
  account_id = "GAHK7EEG2WWHVKDNT4CEQFZGKF2LGDSW2IVM4S5DP42RBW3K6BTODB4A"
  server = Server(horizon_url)
  # Set `join` to `transactions` to include the transactions which created each of the payments in the response.
  resp = server.payments().for_account(account_id).include_failed(False).join("transactions").call()
  print(resp)
  ```

### Version 2.5.0

Released on May 25, 2020

**This update include breaking changes**

In [2.4.0](https://github.com/StellarCN/py-stellar-base/releases/tag/2.4.0), we added support for Stellar Protocol 13, it also includes support for M-strkeys ([SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md)), but now we are going to remove support for [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md), because it is still a draft and may not be promoted to final, adding support for it means that users may end up storing M-strkeys, which can create a lot of problems if [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md) ends up not being implemented. If you want to know more details, please click [here](https://github.com/StellarCN/py-stellar-base/issues/304#issuecomment-632876302).

#### Update

- Revert support for [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md). ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))

#### Breaking changes

- `stellar_sdk.muxed_account.MuxedAccount` has been removed. ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))

- we will no longer accept the M-strkeys address, when resolving the XDR, if it contains a muxed account, only the G-strkeys will be resolved, and the id will be discarded.

- The following fields, which were previously(in 2.4.x) a `stellar_sdk.muxed_account.MuxedAccount` are now a `str` ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))
  - `stellar_sdk.Account.account_id`
  - `stellar_sdk.operation.Operation.source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`

- The following fields, which were previously(in 2.4.x) a `stellar_sdk.muxed_account.MuxedAccount` are now a `stellar_sdk.Keypair` ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))
  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  
### Version 2.5.0-alpha1

Released on May 23, 2020

**This update include breaking changes**

In [2.4.0](https://github.com/StellarCN/py-stellar-base/releases/tag/2.4.0), we added support for Stellar Protocol 13, it also includes support for M-strkeys ([SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md)), but now we are going to remove support for [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md), because it is still a draft and may not be promoted to final, adding support for it means that users may end up storing M-strkeys, which can create a lot of problems if [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md) ends up not being implemented. If you want to know more details, please click [here](https://github.com/StellarCN/py-stellar-base/issues/304#issuecomment-632876302).

#### Update

- Revert support for [SEP-0023](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0023.md). ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))

#### Breaking changes

- `stellar_sdk.muxed_account.MuxedAccount` has been removed. ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))

- we will no longer accept the M-strkeys address, when resolving the XDR, if it contains a muxed account, only the G-strkeys will be resolved, and the id will be discarded.

- The following fields, which were previously(in 2.4.x) a `stellar_sdk.muxed_account.MuxedAccount` are now a `str` ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))
  - `stellar_sdk.Account.account_id`
  - `stellar_sdk.operation.Operation.source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`

- The following fields, which were previously(in 2.4.x) a `stellar_sdk.muxed_account.MuxedAccount` are now a `stellar_sdk.Keypair` ([#319](https://github.com/StellarCN/py-stellar-base/pull/319))
  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  
### Version 2.4.2

Released on May 23, 2020

- refactor: separating client GET and POST timeout values. ([#315](https://github.com/StellarCN/py-stellar-base/pull/315))

- refactor: optimize the use of `stellar_sdk.client.AiohttpClient`, it may throw a `stellar_sdk.exceptions.StreamClientError` exception now, and you should catch it. ([#317](https://github.com/StellarCN/py-stellar-base/pull/317))

  ```python
  import asyncio
  import logging
  
  from stellar_sdk import AiohttpClient, Server
  from stellar_sdk.exceptions import StreamClientError
  
  horizon_url = "https://horizon.stellar.org"
  
  async def listen_transaction():
      async with Server(horizon_url, AiohttpClient()) as server:
          cursor = "now"
          while True:
              try:
                  async for transaction in server.transactions().cursor(cursor).stream():
                      print(f"Transaction: {transaction}")
              except StreamClientError as e:
                  logging.error(f'A StreamClientError was encountered while reading the SSE message, which was caused by {e.current_cursor}.')
                  cursor = e.current_cursor
  
  
  if __name__ == '__main__':
      asyncio.run(listen_transaction())
  ```
  
### Version 2.4.2-alpha2

Released on May 18, 2020

- fix: monkey patch `aiohttp.streams.StreamReader.readline` to solve the problem that `aiohttp_sse_client` cannot read long stream messages.


### Version 2.4.2-alpha1

Released on May 17, 2020

- refactor: separating client GET and POST timeout values. (#315)

- refactor: optimize the use of `stellar_sdk.client.AiohttpClient`, it may throw a `stellar_sdk.exceptions.StreamClientError` exception now, and you should catch it. (#317)

  ```python
  import asyncio
  import logging
  
  from stellar_sdk import AiohttpClient, Server
  from stellar_sdk.exceptions import StreamClientError
  
  horizon_url = "https://horizon.stellar.org"
  
  async def listen_transaction():
      async with Server(horizon_url, AiohttpClient()) as server:
          cursor = "now"
          while True:
              try:
                  async for transaction in server.transactions().cursor(cursor).stream():
                      print(f"Transaction: {transaction}")
              except StreamClientError as e:
                  logging.error(f'A StreamClientError was encountered while reading the SSE message, which was caused by {e.current_cursor}.')
                  cursor = e.current_cursor
  
  
  if __name__ == '__main__':
      asyncio.run(listen_transaction())
  ```


### Version 2.4.1

Released on May 10, 2020

- fix type hint for `stellar_sdk.Server.submit_transaction()`.
- fix broken links in examples.


### Version 2.4.0

Released on May 05, 2020

**This update include breaking changes**.

This version brings protocol 13 support with backwards compatibility support for protocol 12.

#### Added

- Add `stellar_sdk.MuxedAccount` which makes it easy to use muxed account. ([#311](https://github.com/StellarCN/py-stellar-base/pull/311)).
- Add `TransactionBuilder.build_fee_bump_transaction` which makes it easy to create `FeeBumpTransaction`, we have written an example, please click [here](https://github.com/StellarCN/py-stellar-base/blob/91fbd2ad61/examples/build_fee_bump_transaction.py) to view it ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Adds a feature flag which allow consumers of this library to create V1 (Protocol 13) transactions using the `TransactionBuilder` ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add support for [CAP-0027](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0027.md): First-class multiplexed accounts ([#300](https://github.com/StellarCN/py-stellar-base/pull/300)).
- Add `Keypair.xdr_muxed_account` which creates a new `MuxedAccount`([#300](https://github.com/StellarCN/py-stellar-base/pull/300)).
- Add `FeeBumpTransaction` and `FeeBumpTransactionEnvelope` which makes it easy to work with fee bump transactions ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add `stellar_sdk.helpers.parse_transaction_envelope_from_xdr` which makes it easy to parse `TransactionEnvelope` and `FeeBumpTransactionEnvelope`([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).

#### Update

- Update XDR definitions with protocol 13.
- Extend `TransactionEnvelope` to work with `TransactionEnvelope`and `FeeBumpTransactionEnvelope` ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add backward compatibility support for [CAP-0018](https://github.com/stellar/stellar-protocol/blob/f01c9354aaab1e8ca97a25cf888829749cadf36a/core/cap-0018.md) ([#307](https://github.com/StellarCN/py-stellar-base/pull/307)).

#### Breaking changes

- The following fields, which were previously an `str` are now a `stellar_sdk.MuxedAccount` ([#311](https://github.com/StellarCN/py-stellar-base/pull/311)):

  - `stellar_sdk.Account.account_id`
  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  - `stellar_sdk.operation.Operation.source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`

- In this version, some changes have occurred in the XDR files. If you depend on them, please click [here](https://github.com/StellarCN/py-stellar-base/compare/686cf05be3c76426b6386eb31658615aa708b293...30311f51ff0f27f000cf5bc61c5c98ac734eb8f7) to view the changes.

#### Example

Some examples let you quickly learn about these changes.

1. MuxedAccount

   ```python
   from stellar_sdk import MuxedAccount
   
   account_id = "GAQAA5L65LSYH7CQ3VTJ7F3HHLGCL3DSLAR2Y47263D56MNNGHSQSTVY"
   account_id_id = 1234
   account_id_muxed = "MAAAAAAAAAAAJURAAB2X52XFQP6FBXLGT6LWOOWMEXWHEWBDVRZ7V5WH34Y22MPFBHUHY"
   
   # generate account_id_muxed
   muxed = MuxedAccount(account_id=account_id, account_id_id=account_id_id)  # account_id_id is optional.
   print(f"account_id_muxed: {muxed.account_id_muxed}")
   
   # parse account_id_muxed
   muxed = MuxedAccount.from_account(account_id_muxed)
   print(f"account_id: {muxed.account_id}\naccount_id_id: {muxed.account_id_id}")
   
   # without `account_id_id`
   muxed = MuxedAccount.from_account(account_id)
   print(f"account_id_muxed: {muxed.account_id_muxed}")  # None
   ```

2. Pay to muxed account

   ```python
   import pprint
   
   from stellar_sdk import Keypair, Server, MuxedAccount, TransactionBuilder, Network
   
   horizon_url = "http://horizon-testnet.stellar.org/"
   network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
   
   alice_secret = "SC5O7VZUXDJ6JBDSZ74DSERXL7W3Y5LTOAMRF7RQRL3TAGAPS7LUVG3L"
   bob_account = MuxedAccount(
       account_id="GBVKI23OQZCANDUZ2SI7XU7W6ICYKYT74JBXDD2CYRDAFZHZNRPASSQK",
       account_id_id=12387,
   )
   print(f"account_id_muxed: {bob_account.account_id_muxed}")
   
   alice_keypair = Keypair.from_secret(alice_secret)
   
   server = Server(horizon_url=horizon_url)
   alice_account = server.load_account(alice_keypair.public_key)
   transaction = TransactionBuilder(
       source_account=alice_account,
       network_passphrase=network_passphrase,
       base_fee=100,
       v1=True,  # If you want to build Protocol 13 transactions, you need to set `v1` to `True`
   ) \
       .append_payment_op(destination=bob_account, amount="100", asset_code="XLM") \
       .build()
   
   transaction.sign(alice_keypair)
   resp = server.submit_transaction(transaction)
   pprint.pprint(resp) 
   ```

3. Build fee bump transaction

   ```python
   import pprint
   
   from stellar_sdk import Keypair, Server, TransactionBuilder, Network
   from stellar_sdk.exceptions import BadRequestError
   
   horizon_url = "http://horizon-testnet.stellar.org/"
   network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
   
   fee_source_keypair = Keypair.from_secret("SASZKBDB6PFHXN6LRH4NQNTRGLGDTI3PSUVIKMZMLTYYBB7NDVMA6DSL")
   inner_source_keypair = Keypair.from_secret("SC5O7VZUXDJ6JBDSZ74DSERXL7W3Y5LTOAMRF7RQRL3TAGAPS7LUVG3L")
   destination_address = "GBVKI23OQZCANDUZ2SI7XU7W6ICYKYT74JBXDD2CYRDAFZHZNRPASSQK"
   
   server = Server(horizon_url=horizon_url)
   inner_account = server.load_account(inner_source_keypair)
   
   inner_tx = TransactionBuilder(
       source_account=inner_account,
       network_passphrase=network_passphrase,
       base_fee=50,
       v1=True) \
       .append_payment_op(destination=destination_address, amount="100", asset_code="XLM") \
       .build()
   
   inner_tx.sign(inner_source_keypair)
   
   try:
       # This transaction will fail.
       tx_insufficient_fee_resp = server.submit_transaction(inner_tx)
   except BadRequestError as e:
       print(e)
   
   fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
       fee_source=fee_source_keypair,
       base_fee=200,
       inner_transaction_envelope=inner_tx, network_passphrase=network_passphrase
   )
   fee_bump_tx.sign(fee_source_keypair)
   response = server.submit_transaction(fee_bump_tx)
   pprint.pprint(response)
   ```


### Version 2.4.0-alpha2

Released on May 03, 2020

#### Added

- Add `stellar_sdk.MuxedAccount` which makes it easy to use muxed account. ([#311](https://github.com/StellarCN/py-stellar-base/pull/311)).

#### Breaking changes

- The following fields, which were previously an `str` are now a `stellar_sdk.MuxedAccount` ([#311](https://github.com/StellarCN/py-stellar-base/pull/311)):

  - `stellar_sdk.Account.account_id`
  - `stellar_sdk.Transaction.source`
  - `stellar_sdk.FeeBumpTransaction.fee_source`
  - `stellar_sdk.operation.Operation.source`
  - `stellar_sdk.operation.AccountMerge.destination`
  - `stellar_sdk.operation.AllowTrust.destination`
  - `stellar_sdk.operation.PathPaymentStrictReceive.destination`
  - `stellar_sdk.operation.PathPaymentStrictSend.destination`
  - `stellar_sdk.operation.PathPayment.destination`
  - `stellar_sdk.operation.Payment.destination`


### Version 2.3.2
Released on May 01, 2020

- fix: typo in fetching previous page.([#312](https://github.com/StellarCN/py-stellar-base/issues/312))


### Version 2.4.0-alpha1

Released on April 26, 2020

**This update include breaking changes**.

This version brings protocol 13 support with backwards compatibility support for protocol 12.

#### Added

- Add `TransactionBuilder.build_fee_bump_transaction` which makes it easy to create `FeeBumpTransaction`, we have written an example, please click [here](https://github.com/StellarCN/py-stellar-base/blob/91fbd2ad61/examples/build_fee_bump_transaction.py) to view it ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Adds a feature flag which allow consumers of this library to create V1 (Protocol 13) transactions using the `TransactionBuilder` ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add support for [CAP-0027](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0027.md): First-class multiplexed accounts ([#300](https://github.com/StellarCN/py-stellar-base/pull/300)).
- Add `Keypair.xdr_muxed_account` which creates a new `MuxedAccount`([#300](https://github.com/StellarCN/py-stellar-base/pull/300)).
- Add `FeeBumpTransaction` and `FeeBumpTransactionEnvelope` which makes it easy to work with fee bump transactions ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add `stellar_sdk.helpers.parse_transaction_envelope_from_xdr` which makes it easy to parse `TransactionEnvelope` and `FeeBumpTransactionEnvelope`([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).

#### Update

- Update XDR definitions with protocol 13.
- Extend `TransactionEnvelope` to work with `TransactionEnvelope`and `FeeBumpTransactionEnvelope` ([#298](https://github.com/StellarCN/py-stellar-base/pull/298)).
- Add backward compatibility support for [CAP-0018](https://github.com/stellar/stellar-protocol/blob/f01c9354aaab1e8ca97a25cf888829749cadf36a/core/cap-0018.md) ([#307](https://github.com/StellarCN/py-stellar-base/pull/307)).

#### Breaking changes

- The type of `Transaction.source` changes from `Keypair` to `str`.

- In this version, some changes have occurred in the XDR files. If you depend on them, please click [here](https://github.com/StellarCN/py-stellar-base/compare/686cf05be3c76426b6386eb31658615aa708b293...30311f51ff0f27f000cf5bc61c5c98ac734eb8f7) to view the changes.

- The following XDR fields, which were previously an `AccountID` are now a `MuxedAccount` ([#300](https://github.com/StellarCN/py-stellar-base/pull/300)):

  - `PaymentOp.destination`
  - `PathPaymentStrictReceiveOp.destination`
  - `PathPaymentStrictSendOp.destination`
  - `OperationOp.source`
  - `Operation.destination` (for `ACCOUNT_MERGE`)
  - `Transaction.source`
  - `FeeBumpTransaction.feeSource`

  You can get the string representation by calling `StrKey.encode_muxed_account` which will return a `G..` or `M..` account.

### Version 2.3.1
Released on April 12, 2020

- Update dependencies.

### Version 2.3.0
Released on March 31, 2020

#### Added
- Add SEP0029 (memo required) support. ([#291](https://github.com/StellarCN/py-stellar-base/pull/291))
  Extends `Server.submit_transaction` to always run a memo required check before 
  sending the transaction. If any of the destinations require a memo and the 
  transaction doesn't include one, then an `AccountRequiresMemoError` will be thrown.
  
  This may degrade performance, but you can skip this check by passing `skip_memo_required_check=True` to `Server.submit_transaction`:

  ```
  server.submit_transaction(tx, skip_memo_required_check=True)
  ```
  The check runs for each operation of type:
    - `Payment`
    - `PathPaymentStrictReceive`
    - `PathPaymentStrictSend`
    - `AccountMerge`
  
  If the transaction includes a memo, then memo required checking is skipped.
  
  See [SEP-0029](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0029.md) for more information about memo required check.

#### Changed
- Optimize the processing of horizon parameters. ([#289](https://github.com/StellarCN/py-stellar-base/pull/289))

### Version 2.2.3
Released on March 12, 2020

* feat: add `stellar_sdk.operation.set_options.Flag`, we can express flag more conveniently. ([fdb1f7d](https://github.com/StellarCN/py-stellar-base/commit/fdb1f7da42c2c6307fa91b010addc9535c77b7d5))

### Version 2.2.2
Released on March 08, 2020

* fix: parameters checking rule in TimeBounds. ([561f3e7](https://github.com/StellarCN/py-stellar-base/commit/561f3e7a3c407783eb8ecbed4134978fd88497f4))
* fix: HashMemo and ReturnHashMemo should be fixed in length (32 bytes). ([22cd179](https://github.com/StellarCN/py-stellar-base/commit/22cd1794ea7c35b059549588893c410b6fd297d8))

### Version 2.2.1
Released on February 12, 2020

* fix: orderbook async streams (#265)

### Version 2.2.0
Released on February 07, 2020

Horizon v1.0.0 Compatibility.

#### Added

- Add support for top-level offers endpoint with `seller`, `selling`, and `buying` filter.
  Horizon 1.0 includes a new `/offers` end-point, which allows you to list all offers, supporting filtering by `seller`, `selling`, or `buying` asset.

  You can fetch data from this endpoint by doing `server.offers()` and use any of the following filters:

  - `seller`: `server.offers().for_seller(account_id)`
  - `buying`: `server.offers().for_buying(asset)`
  - `selling`: `server.offers().for_selling(asset)`
  - `offer detail` : `server.offers().offer(offer_id)`

  This introduced a breaking change since it modified the signature for the function `server.offers()`.

  Before, if you wanted to list all the offers for a given account, you'd do:

  ```
  server.offers(account_id)
  ```

  Starting on this version you'll need to do:

  ```
  server.offers().for_seller(account_id)
  ```

  You can do now things that were not possible before, like finding
  all offers for an account filtering by the selling or buying asset

  ```
  server.offers().for_seller(account_id).for_buying(buying_asset).for_selling(selling_asset)
  ```

- Add support for filtering accounts by `signer` or `asset`, this has been released in a previous patch version.
  Horizon 1.0 includes a new `/accounts` end-point, which allows you to list all accounts who have another account as a signer or hold a given asset.

  You can fetch data from this endpoint by doing `server.accounts()` and use any of the following filters:

  - `acount detail`: `server.accounts().account_id(account_id)`, returns a single account.
  - `for signer`: `server.accounts().for_signer(account_id)`, returns accounts where `account_id` is a signer.
  - `for asset`: `server.accounts().for_asset(asset)`, returns accounts which hold the `asset`.

#### Changed

- Regenerate the XDR definitions to include [MetaV2](https://github.com/jonjove/stellar-core/blob/b299b3a458a15f592352c67d4da69baa6e8fbb6a/src/xdr/Stellar-ledger.x#L309) support (also see [#1902](https://github.com/stellar/go/issues/1902)).

#### Fixed

- Fixed some documentation errors.

#### Breaking

- Change function signature for `server.offers`. 
  The signature for the function `server.offers()` was changed to bring support for other filters.

  Before, if you wanted to list all the offers for a given account, you'd do:

  ```
  server.offers(account_id)
  ```

  Starting on this version you'll need to do:

  ```
  server.offers().for_seller(account_id)
  ```

* `server.accounts().signer` and `server.accounts().asset` are marked as deprecated, use `server.accounts().for_signer` and `server.accounts().for_asset` instead.

There are also some changes related to the horizon's response, currently, SDK has not added parse support to it, 
so please refer to this [issue](https://github.com/StellarCN/py-stellar-base/issues/257) or release notes of Stellar horizon 1.0.0. In addition, support for parsing the horizon's responses will be added in the next major update.

### Version 2.1.4
Released on February 12, 2020

* fix: orderbook async streams (#265)

### Version 2.1.3
Released on February 03, 2020

* fix: fix bug in SEP-0010 implementation.

### Version 2.1.2
Released on February 02, 2020

* fix: fix bug in SEP-0010 implementation.

### Version 2.1.1
Released on January 31, 2020

* feat: update challenge tx helpers for SEP-0010 v1.3.0.

### Version 2.1.0
Released on January 04, 2020

* feat: add support for SEP-0001 (stellar.toml).
* feat: add support for SEP-0002 (Federation protocol).
* perf: adjust the client's default timeout.

### Version 2.0.0
Released on November 29, 2019

This is a major upgrade and is not compatible with the v1.x version, 
don't worry, the v1.x version will still be maintained. 

Anyway, welcome to the v2.0.0 release, 
we have a [great document](https://stellar-sdk.readthedocs.org/) to help you get started. 

If you have suggestions, feel free to submit an issue or email me. Thank you for your patience as we transition!

New features: 
- New API design. We refactored most of the code, there are a lot of designs in v1.x that are not reasonable, 
and we can't modify them smoothly, this is one of the reasons we released v2.x.
- Added type hint support.
- Added asynchronous support.