pragma solidity >=0.4.0 <0.9.0;
contract Rating {
        function setRating(bytes32 _key, uint256 _value) {
            ratings[_key] = _value;
        }
        mapping (bytes32 => uint256) public ratings;
    }