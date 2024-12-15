// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity <= 0.8.17;
pragma abicoder v2;

import "./console.sol";
import "./TransferHelper.sol";
import './ISwapRouter.sol';

contract UniSwapExamples {
    // For the scope of these swap examples,
    // we will detail the design considerations when using
    // `exactInput`, `exactInputSingle`, `exactOutput`, and  `exactOutputSingle`.

    // It should be noted that for the sake of these examples, we purposefully pass in the swap router instead of inherit the swap router for simplicity.
    // More advanced example contracts will detail how to inherit the swap router safely.

    ISwapRouter public immutable swapRouter;

    // For this example, we will set the pool fee to 0.3%.
    uint24 public constant poolFee = 500;

    constructor(ISwapRouter _swapRouter) {
        swapRouter = _swapRouter;
    }

    function swapExactInputSingle(address _tokenIn,address _tokenOut,uint256 _amountIn) external returns (uint256 amountOut) {
        // msg.sender must approve this contract

        console.log("msg.sender address: %s",msg.sender);
        // Transfer the specified amount of DAI to this contract.
        TransferHelper.safeTransferFrom(_tokenIn, msg.sender, address(this), _amountIn);
        console.log("balance send from sendr: %s",address(this).balance);
        // Approve the router to spend DAI.
        TransferHelper.safeApprove(_tokenIn, address(swapRouter), _amountIn);
        console.log("PASS APPROVE");
        // Naively set amountOutMinimum to 0. In production, use an oracle or other data source to choose a safer value for amountOutMinimum.
        // We also set the sqrtPriceLimitx96 to be 0 to ensure we swap our exact input amount.
        ISwapRouter.ExactInputSingleParams memory params =
            ISwapRouter.ExactInputSingleParams({
                tokenIn: _tokenIn,
                tokenOut: _tokenOut,
                fee: poolFee,
                recipient: msg.sender,
                deadline: block.timestamp,
                amountIn: _amountIn,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        // The call to `exactInputSingle` executes the swap.
        amountOut = swapRouter.exactInputSingle(params);
    }
}