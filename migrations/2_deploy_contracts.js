
// const FlashLoan = artifacts.require("FlashLoanSwapTest");
// const FlashLoan2 = artifacts.require("FlashLoanTest2");
// const OninchSwap = artifacts.require("SwapProxy");
// const Duoswap = artifacts.require("DuoswapTest");
// const FlashLoanArb = artifacts.require("FlashLoanArb");
// const FlashLoanArb0x = artifacts.require("FlashLoanArb0x");
// const sushi_swap = artifacts.require("sushi_swap");
// const UniSwapExamples = artifacts.require("UniSwapExamples");
const Quickswap = artifacts.require("Quickswap");
// const FlashBorrowerExample = artifacts.require("FlashBorrowerExample");
// const FlashloanBorrower = artifacts.require("FlashloanBorrower");
const AaveFlashLoan = artifacts.require("AaveFlashloan");
// const eventTest = artifacts.require("eventTest");
// const AbiDecodeTest = artifacts.require("AbiDecodeTest");
const LendingPoolAddressesProvider_Polygon_V3 = '0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb'; //Polygon V3
const LendingPoolAddressesProvider_Polygon_V2 = '0xd05e3E715d945B59290df0ae8eF85c1BdB684744'; //Polygon V2

const Uniswap_V3_Factory = '0x1F98431c8aD98523631AE4a59f267346ea31F984';
const Uniswap_V3_Router = '0xE592427A0AEce92De3Edee1F18E0157C05861564';
const sushiRouter = '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F';
const swapRouter = '0xE592427A0AEce92De3Edee1F18E0157C05861564';
const AavePoolAddressesProvider = '0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb';

module.exports = async function(deployer) {
    deployer.then(async () => {

        // Deploy FlashLoan contract
        // await deployer.deploy(FlashLoan, LendingPoolAddressesProvider_Polygon, { gas: 5000000 });
        // const FlashLoanContract = await FlashLoan.deployed();
        // console.log("FlashLoan deployement done:", FlashLoanContract.address);

        // await deployer.deploy(AbiDecodeTest, { gas: 5000000 });
        // const AbiDecodeTestContract = await AbiDecodeTest.deployed();
        // console.log("FlashLoanArb0x deployement done:", AbiDecodeTestContract.address);

        // await deployer.deploy(sushi_swap, Uniswap_V3_Factory, Uniswap_V3_Router, sushiRouter, { gas: 5000000 });
        // const Contract = await sushi_swap.deployed();
        // console.log("sushi_swap deployement done:", Contract.address);

        // await deployer.deploy(UniSwapExamples, swapRouter, { gas: 5000000 });
        // const UniSwapContractAddress = await UniSwapExamples.deployed();
        // console.log("UniSwapExamples deployement done:", UniSwapContractAddress.address);

        await deployer.deploy(Quickswap, { gas: 5000000 });
        const Quickswap_Contract = await Quickswap.deployed();
        console.log("Quickswap deployement done:", Quickswap_Contract.address);

        // await deployer.deploy(FlashloanBorrower, { gas: 5000000 });
        // const FlashloanBorrower_Contract = await FlashloanBorrower.deployed();
        // console.log("FlashloanTest_Contract deployement done:", FlashloanBorrower_Contract.address);

        // await deployer.deploy(eventTest, { gas: 5000000 });
        // const eventTest_Contract = await eventTest.deployed();
        // console.log("eventTest_Contract deployement done:", eventTest_Contract.address);

        await deployer.deploy(AaveFlashLoan, LendingPoolAddressesProvider_Polygon_V3, Uniswap_V3_Router, { gas: 5000000 });
        const AaveFlashLoan_Contract = await AaveFlashLoan.deployed();
        console.log("AaveFlashLoan_Contract deployement done:", AaveFlashLoan_Contract.address);

        // await deployer.deploy(FlashBorrowerExample, swapRouter, { gas: 5000000 });
        // const FlashloanTest_Contract = await FlashBorrowerExample.deployed();
        // console.log("FlashloanTest_Contract deployement done:", FlashloanTest_Contract.address);

        // await deployer.deploy(FlashLoanArb0x, LendingPoolAddressesProvider_Polygon, { gas: 5000000 });
        // const Contract = await FlashLoanArb0x.deployed();
        // console.log("FlashLoanArb0x deployement done:", Contract.address);

        // await deployer.deploy(FlashLoanArb, LendingPoolAddressesProvider_Polygon, { gas: 5000000 });
        // const FlashLoanArbContract = await FlashLoanArb.deployed();
        // console.log("FlashLoanArb deployement done:", FlashLoanArbContract.address);

        // await deployer.deploy(Duoswap, { gas: 5000000 });
        // const DuoswapContract = await Duoswap.deployed();
        // console.log("Duoswap deployement done:", DuoswapContract.address);

        // await deployer.deploy(FlashLoan2, LendingPoolAddressesProvider_Polygon, { gas: 5000000 });
        // const FlashLoanContract2 = await FlashLoan2.deployed();
        // console.log("FlashLoan2 deployement done:", FlashLoanContract2.address);

        // await deployer.deploy(OninchSwapTest, { gas: 5000000 });
        // const FlashLoanContract = await OninchSwapTest.deployed();
        // console.log("FlashLoan deployement done:", FlashLoanContract.address);

        // await deployer.deploy(FlashLoan, LendingPoolAddressesProvider_Polygon, { gas: 5000000 });
        // const FlashLoanContract = await FlashLoan.deployed();
        // console.log("FlashLoan deployement done:", FlashLoanContract.address);

        // await deployer.deploy(OninchSwap, { gas: 5000000 });
        // const SwapProxyContract = await OninchSwap.deployed();
        // console.log("SwapProxy deployement done:", SwapProxyContract.address);

        const fs = require('fs');
        const AppSettings = JSON.parse(fs.readFileSync("./scripts/AppSettings.json"));
        // AppSettings.Local.FlashLoanArbContractAddress = Contract.address;
        AppSettings.Local.QuickswapContractAddress = Quickswap_Contract.address;
        // AppSettings.Local.UniswapContractAddress = UniSwapContractAddress.address;
        // AppSettings.Polygon.AaveFlashLoan_ContractAddress = AaveFlashLoan_Contract.address;
        AppSettings.Local.AaveFlashLoan_ContractAddress = AaveFlashLoan_Contract.address;
        // AppSettings.Local.eventTest_ContractAddress = eventTest_Contract.address;
        // AppSettings.Local.FlashloanTest_ContractAddress = FlashloanTest_Contract.address;
        // AppSettings.Local.FlashloanBorrower_ContractAddress = FlashloanBorrower_Contract.address;
        fs.writeFileSync("./scripts/AppSettings.json", JSON.stringify(AppSettings, null, 4));
        console.log('Contract address Updated!');
    });
};