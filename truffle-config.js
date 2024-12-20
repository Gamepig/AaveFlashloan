/**
 * Use this file to configure your truffle project. It's seeded with some
 * common settings for different networks and features like migrations,
 * compilation and testing. Uncomment the ones you need or modify
 * them to suit your project as necessary.
 *
 * More information about configuration can be found at:
 *
 * trufflesuite.com/docs/advanced/configuration
 *
 * To deploy via Infura you'll need a wallet provider (like @truffle/hdwallet-provider)
 * to sign your transactions before they're sent to a remote public node. Infura accounts
 * are available for free at: infura.io/register.
 *
 * You'll also need a mnemonic - the twelve word phrase the wallet uses to generate
 * public/private key pairs. If you're publishing your code to GitHub make sure you load this
 * phrase from a file you've .gitignored so it doesn't accidentally become public.
 *
 */

// const HDWalletProvider = require('@truffle/hdwallet-provider');
//
// const fs = require('fs');
// const mnemonic = fs.readFileSync(".secret").toString().trim();
const HDWalletProvider = require("@truffle/hdwallet-provider");
require("dotenv").config();
const privateKey = 'c5f5b4c1575d03c2960567ee70c325151b46db3762cdf0694301509ded6e0db1';
module.exports = {
    /**
     * Networks define how you connect to your ethereum client and let you set the
     * defaults web3 uses to send transactions. If you don't specify one truffle
     * will spin up a development blockchain for you on port 9545 when you
     * run `develop` or `test`. You can ask a truffle command to use a specific
     * network from the command line, e.g
     *
     * $ truffle test --network <network-name>
     */
    // contracts_directory: "./contracts/FlashLoanSwapTest.sol",
    networks: {
        // Useful for testing. The `development` name is special - truffle uses it by default
        // if it's defined here and no other network is specified at the command line.
        // You should run a client (like ganache-cli, geth or parity) in a separate terminal
        // tab if you use this network and you must also set the `host`, `port` and `network_id`
        // options below to some value.
        //
        development: {
            host: "127.0.0.1", // Localhost (default: none)
            port: 8545, // Standard Ethereum port (default: none)
            network_id: "*", // Any network (default: none)
        },
        solc: {
            optimizer: {
                enabled: true,
                runs: 200
            }
        },
        // polygon: {
        //     provider: new HDWalletProvider(process.env.DEPLOYMENT_ACCOUNT_KEY, "https://polygon-mainnet.infura.io/v3/" + process.env.INFURA_API_KEY),
        //     network_id: 137,
        //     gas: 5000000,
        //     gasPrice: 50000000000, // 50 Gwei
        //     from: '0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a',
        //     skipDryRun: true
        // },
        polygon: {
            // provider: new HDWalletProvider(process.env.DEPLOYMENT_ACCOUNT_KEY, "https://polygon-rpc.com/"),
            provider: new HDWalletProvider(privateKey, "https://polygon-rpc.com/"),
            network_id: 137,
            gas: 5000000,
            gasPrice: 50000000000, // 50 Gwei
            from: '0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a',
            skipDryRun: true
        },
        mumbai: {
            provider: new HDWalletProvider(process.env.DEPLOYMENT_ACCOUNT_KEY, "https://polygon-mumbai.infura.io/v3/" + process.env.INFURA_API_KEY),
            network_id: 80001,
            gas: 5000000,
            gasPrice: 10000000000, // 10 Gwei
            from: '0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a',
            skipDryRun: true
        },
        mainnet: {
            provider: new HDWalletProvider(process.env.DEPLOYMENT_ACCOUNT_KEY, "https://mainnet.infura.io/v3/" + process.env.INFURA_API_KEY),
            network_id: 1,
            gas: 5000000,
            gasPrice: 5000000000 // 5 Gwei
        }
    },

    // Set default mocha options here, use special reporters etc.
    mocha: {
        // timeout: 100000
    },

    // Configure your compilers
    compilers: {
        solc: {
            version: "0.8.10", // Fetch exact version from solc-bin (default: truffle's version)
            docker: false, // Use "0.5.1" you've installed locally with docker (default: false)
            settings: { // See the solidity docs for advice about optimization and evmVersion
                optimizer: {
                    enabled: false,
                    runs: 200
                },
                //  evmVersion: "byzantium"
                // }
            }
        }

        // Truffle DB is currently disabled by default; to enable it, change enabled:
        // false to enabled: true. The default storage location can also be
        // overridden by specifying the adapter settings, as shown in the commented code below.
        //
        // NOTE: It is not possible to migrate your contracts to truffle DB and you should
        // make a backup of your artifacts to a safe location before enabling this feature.
        //
        // After you backed up your artifacts you can utilize db by running migrate as follows: 
        // $ truffle migrate --reset --compile-all
        //
        // db: {
        // enabled: false,
        // host: "127.0.0.1",
        // adapter: {
        //   name: "sqlite",
        //   settings: {
        //     directory: ".db"
        //   }
        // }
        // }
    }
};