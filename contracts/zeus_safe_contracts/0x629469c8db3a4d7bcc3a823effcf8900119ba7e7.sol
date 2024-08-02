pragma solidity >=0.4.0 <0.9.0;
contract BeerKeg {
    bytes20 prev; // Nickname of the previous tap attempt
    function tap(bytes20 nickname) {
        prev = nickname;
        if (prev != nickname) {
          msg.sender.send(this.balance);
        }
    }
}