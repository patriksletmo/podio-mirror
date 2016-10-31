# podio-mirror
## Introduction
The library podio-mirror aims to mitigate the Podio API request limit 
and performance issues by caching the used data locally. Most returned 
data maintains the format returned by the bare API and can be used 
universally.

## Design
podio-mirror is designed with traceability in mind and all changed data
is stored as atomic transactions. When refreshing data from Podio all
local changes are pushed upstream and merged with the remote data, while
also maintaining changes performed directly in Podio. The current data
is then downloaded from Podio again and replaces what's downloaded to
ensure that the assumptions made of the Podio behaviour does not cause 
any critical issues.

## Disclaimer
The library in its current state contains various problems and does not
include the created implementations for using the library with a Django 
database. There are also no good validations to ensure that the changes 
are executed correctly. Use the code at your own risk.
