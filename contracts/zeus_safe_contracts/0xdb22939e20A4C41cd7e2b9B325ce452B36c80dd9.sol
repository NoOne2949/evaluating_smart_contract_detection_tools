pragma solidity >=0.4.0 <0.9.0;
contract AlwaysFail {
    function AlwaysFail() {
    }

    function() {
        enter();
    }

    function enter() {
        throw;
    }
}