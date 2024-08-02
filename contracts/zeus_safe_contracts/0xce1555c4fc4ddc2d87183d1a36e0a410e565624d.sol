pragma solidity >=0.4.0 <0.9.0;contract storadge {
    event log(string description);
	function save(
        string mdhash
    )
    {
        log(mdhash);
    }
}