// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity <= 0.8.17;

import "../contracts/console.sol";
import "../contracts/IERC20.sol";
import "../contracts/TransferHelper.sol";
import '../contracts/IUniswapRouterV2.sol';

contract Quickswap{
    address public constant ROUTER = 0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff;
    
    function swap_quickswap(address _tokenIn,address _tokenOut,uint256 amount) public {
        
        IERC20 fromtokenContract = IERC20(_tokenIn);

        TransferHelper.safeTransferFrom(_tokenIn, msg.sender, address(this), amount);

        require(fromtokenContract.approve(ROUTER, amount), 'approve failed.');
        
        address[] memory path;
        path = new address[](2);
        path[0] = _tokenIn ;
        path[1] = _tokenOut;
        IUniswapRouterV2(ROUTER).swapExactTokensForTokens(amount, 1, path, msg.sender, block.timestamp);
    }
}