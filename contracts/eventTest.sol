	// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract eventTest {
   event eTest(uint256 val);
   uint256 val;
   function Test(uint256 _val) public {
         val = _val;
         emit eTest(val);
  }
}