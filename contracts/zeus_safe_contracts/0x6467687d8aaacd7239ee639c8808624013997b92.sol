pragma solidity >=0.4.0 <0.9.0;
contract SimpleStorage {
  uint storedData;
  function set(uint x) {
    storedData = x;
  }

  function get() constant returns (uint retVal) {
    return storedData;
  }
}