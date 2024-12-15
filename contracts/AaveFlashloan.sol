// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import { FlashLoanSimpleReceiverBase } from './FlashLoanSimpleReceiverBase.sol';
import { IPoolAddressesProvider } from '../interfaces/IPoolAddressesProvider.sol';
import { IPool } from '../interfaces/IPool.sol';
import { IERC20 } from '../interfaces/IERC20.sol';
import '../contracts/IUniswapRouterV2.sol';
import "./console.sol";
import './ISwapRouter.sol';

contract AaveFlashLoan is FlashLoanSimpleReceiverBase {
    event ReturnAmouint(uint256 _ReturnAmouint);
    address __tokenOut;
    uint  DEX1;
    uint  DEX2;
    uint  _ReturnAmouint;
    ISwapRouter public immutable swapRouter;
    address public constant QuickSwap_ROUTER = 0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff;
    address public constant SushiSwap_ROUTER = 0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506;
    address public constant ApeSwap_ROUTER = 0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607;
    // For this example, we will set the pool fee to 0.01%.
    uint24 public constant poolFee = 500;
    constructor(IPoolAddressesProvider _provider, ISwapRouter _swapRouter) FlashLoanSimpleReceiverBase(_provider) {swapRouter = _swapRouter;}

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
    //   any actions that need to be performed by the loan goes here
    uint256 totalOwed = amount + premium;
    console.log("asset: %s",IERC20(asset).balanceOf(address(this)));

    if(DEX1==0){
        swapExactInputSingle(asset,__tokenOut,amount);
    }else if(DEX1==1){
        swap_quickswap(asset,__tokenOut,amount);
    }else if(DEX1==2){
        swap_SushiSwap(asset,__tokenOut,amount);
    }else if(DEX1==3){
        swap_ApeSwap(asset,__tokenOut,amount);
    }

    if(DEX2==0){
        swapExactInputSingle(asset,__tokenOut,amount);
    }else if(DEX2==1){
        swap_quickswap(asset,__tokenOut,amount);
    }else if(DEX2==2){
        swap_SushiSwap(asset,__tokenOut,amount);
    }else if(DEX2==3){
        swap_ApeSwap(asset,__tokenOut,amount);
    }

    require(IERC20(asset).balanceOf(address(this)) > totalOwed, "NOT enough token to paid back!");
    // Approve the pool to deduct the amount owed from the contract
    IERC20(asset).approve(address(POOL), totalOwed);

    uint256 sendBackToken = IERC20(asset).balanceOf(address(this)) - totalOwed;
    console.log("sendBackToken: %s",sendBackToken);
    address MainAccount = 0x85D6EceC4F3cD8AE8DF22dcE8437085B4C2A1E4a;
    // address MainAccount = 0x32d55Dd4EAe334110c26Ecb3217AF267117922D3;
    IERC20(asset).approve(address(this), sendBackToken);
    IERC20(asset).transfer(MainAccount,sendBackToken);
    emit ReturnAmouint(sendBackToken);
    return true;
  }

  function getFlashLoan(
        address asset,
        address _tokenOut,
        uint256 amount,
        uint    _DEX1,
        uint    _DEX2
    ) public {
        address receiverAddress = address(this);

        bytes memory params = "";
        uint16 referralCode = 0;
        __tokenOut = _tokenOut;
        DEX1 = _DEX1;
        DEX2 = _DEX2;

        POOL.flashLoanSimple(
            receiverAddress,
            asset,
            amount,
            params,
            referralCode
        );
    }

    function swap_ApeSwap(address _tokenIn,address _tokenOut,uint256 amount) internal {
        
        require(IERC20(_tokenIn).approve(ApeSwap_ROUTER, amount), 'approve failed.');
        
        address[] memory path;
        path = new address[](2);
        path[0] = _tokenIn ;
        path[1] = _tokenOut;
        IUniswapRouterV2(ApeSwap_ROUTER).swapExactTokensForTokens(amount, 1, path, address(this), block.timestamp);
    }

    function swap_SushiSwap(address _tokenIn,address _tokenOut,uint256 amount) internal {
        
        require(IERC20(_tokenIn).approve(SushiSwap_ROUTER, amount), 'approve failed.');
        
        address[] memory path;
        path = new address[](2);
        path[0] = _tokenIn ;
        path[1] = _tokenOut;
        IUniswapRouterV2(SushiSwap_ROUTER).swapExactTokensForTokens(amount, 1, path, address(this), block.timestamp);
    }

    function swap_quickswap(address _tokenIn,address _tokenOut,uint256 amount) internal {
        
        require(IERC20(_tokenIn).approve(QuickSwap_ROUTER, amount), 'approve failed.');
        
        address[] memory path;
        path = new address[](2);
        path[0] = _tokenIn ;
        path[1] = _tokenOut;
        IUniswapRouterV2(QuickSwap_ROUTER).swapExactTokensForTokens(amount, 1, path, address(this), block.timestamp);
    }

    function swapExactInputSingle(address _tokenIn,address _tokenOut,uint256 _amountIn) internal {
        // address UniswapRouterV3 = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
        // Approve the router to spend tokenIn.
        IERC20(_tokenIn).approve(address(swapRouter), _amountIn);

        ISwapRouter.ExactInputSingleParams memory params =
            ISwapRouter.ExactInputSingleParams({
                tokenIn: _tokenIn,
                tokenOut: _tokenOut,
                fee: poolFee,
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: _amountIn,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        // The call to `exactInputSingle` executes the swap.
        swapRouter.exactInputSingle(params);
    }

}