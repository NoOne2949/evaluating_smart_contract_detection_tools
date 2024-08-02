pragma solidity >=0.4.0 <0.9.0;contract owned {
  function owned() {
    owner = msg.sender;
  }
  modifier onlyowner() {
    if (msg.sender == owner)
    _
  }
  function kill() {  //remove in production
    if (msg.sender == owner)
    suicide(owner);
  }
  function transfer(address addr) {
    if (msg.sender == owner)
      owner = addr;
  }
  address public owner;
}