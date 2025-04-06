User Study
Thanks for taking part in our user study. I will give 12 smart contract cases, you should check them and determine if it is vulnerable. You should answer yes or no while identifying the smart contract. Please repair and output the result if you find the smart contract is vulnerable.

Note: The maximum time for each smart contract is 10 minutes per task, if time’s over, please give up the current task and denote the consumed time as “over 10 minutes”

Here is an overview of the questions:
(1)	Is the smart contract vulnerable? Please answer yes or no.
(2)	Please repair it and output the result if you identify the smart contract is vulnerable.
(3)	Please record the time you spent on detecting and repairing this smart contract (seconds).
(4)	What is the difficulty of the smart contract do you think? (you should answer easy, medium, hard)
(5)	Does the suggestion provided can help you detect and repair the smart contract? If yes, tell me the reason.

Let’s begin the user study.
==================================================================
Case 1:
Here is our suggestion on this case:
Detection result: Yes
Potentially vulnerable code:
function Collect(uint _am)
if(msg.sender.call.value(_am)())
Repair Approach: you can fix the reentrancy vulnerability by replacing the ‘call.value’ with ‘transfer’ or ‘send’.
Vulnerable Example: 
1.	function withdraw(uint256 amount) public {  
2.	    require(balances[msg.sender] >= amount, "Insufficient balance");  
3.	    (bool success, ) = msg.sender.call.value(amount);  
4.	    require(success, "Transfer failed");  
5.	    balances[msg.sender] -= amount;  
6.	} 
Fixed Example: 
1.	function withdraw(uint256 amount) public {  
2.	    require(balances[msg.sender] >= amount, "Insufficient balance"); 
3.	    (bool success, ) = msg.sender.transfer(amount);  
4.	    require(success, "Transfer failed");  
5.	    balances[msg.sender] -= amount;  
6.	}

Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 2:
Here is our suggestion on this case:
Detection result: Yes
Potentially vulnerable code:
        if(_am<=balances[msg.sender])
            if(msg.sender.call.value(_am)())
Repair Approach: you can fix reentrancy vulnerability by locking the code gadgets, which include ‘call.value’.
Vulnerable Example: 
1.	function withdraw(uint256 amount) public {    
2.	    require(balances[msg.sender] >= amount, "Insufficient balance");    
3.	    (bool success, ) = msg.sender.call.value(amount);    
4.	    require(success, "Transfer failed");    
5.	    balances[msg.sender] -= amount;    
6.	}  
Fixed Example: 
1.	function withdraw(uint256 amount) public {  
2.	    require(!locked, "Reentrancy detected");    
3.	    locked = true;    
4.	    require(balances[msg.sender] >= amount, "Insufficient balance");  
5.	    (bool success, ) = msg.sender.call{value: amount}("");  
6.	    require(success, "Transfer failed");  
7.	    balances[msg.sender] -= amount;  
8.	    locked = false;   
9.	}  
Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 3:
Here is our suggestion on this case:
Detection result: yes
Potentially vulnerable code:
    if(balances[msg.sender] >= _amount) {
      if(msg.sender.call.value(_amount)()) {
Repair Approach: you can fix reentrancy vulnerability by using the "checks-effects-interactions" model.
Vulnerable Example: 
1.	function withdraw(uint256 amount) public {      
2.	    require(balances[msg.sender] >= amount, "Insufficient balance");      
3.	    (bool success, ) = msg.sender.call.value(amount);      
4.	    require(success, "Transfer failed");      
5.	    balances[msg.sender] -= amount;      
6.	} 
Fixed Example: 
1.	function withdraw(uint256 amount) public {  
2.	    require(balances[msg.sender] >= amount, "Insufficient balance");  
3.	    balances[msg.sender] -= amount;  
4.	    (bool success, ) = msg.sender.call.value(amount);  
5.	    require(success, "Transfer failed");  
6.	}  
Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 4:
Here is our suggestion on this case:
Detection result: yes
Potentially vulnerable code:
function withdrawFunds (uint256 _weiToWithdraw) public {
        require(balances[msg.sender] >= _weiToWithdraw);
        require(msg.sender.call.value(_weiToWithdraw)());
Repair Approach: you can fix the reentrancy vulnerability by replacing the ‘call.value’ with ‘transfer’ or ‘send’.
Vulnerable Example: 
7.	function withdraw(uint256 amount) public {  
8.	    require(balances[msg.sender] >= amount, "Insufficient balance");  
9.	    (bool success, ) = msg.sender.call.value(amount);  
10.	    require(success, "Transfer failed");  
11.	    balances[msg.sender] -= amount;  
12.	} 
Fixed Example: 
7.	function withdraw(uint256 amount) public {  
8.	    require(balances[msg.sender] >= amount, "Insufficient balance"); 
9.	    (bool success, ) = msg.sender.transfer(amount);  
10.	    require(success, "Transfer failed");  
11.	    balances[msg.sender] -= amount;  
12.	}
Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 5:
Here is our suggestion on this case:
Detection result: No
Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 6:
Here is our suggestion on this case:
Detection result: No
Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 7:
Here is our suggestion on this case:
Detection result: No
Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 8:
Here is our suggestion on this case:
Detection result: No
Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 9:
Here is our suggestion on this case:
Detection result: No
Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 10:
Here is our suggestion on this case:
Detection result: No

Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 11:
Here is our suggestion on this case:
Detection result: Yes
Potentially vulnerable code:
        if (etherHero.call.value(address(this).balance).gas(estGas)()) {
            investFund = address(this).balance;
            stubF.call.value(calcStubFundPercent).gas(estGas)();
Repair Approach: you can fix the reentrancy vulnerability by replacing the ‘call.value’ with ‘transfer’ or ‘send’.
Vulnerable Example: 
1.	function processWithdrawal(uint256 value) public {    
2.	    if (balances[msg.sender] > value) {  
3.	        (bool success, ) = msg.sender.call.value(value);      
4.	        require(success, "Transfer failed");  
5.	        balances[msg.sender] -= value; }    
6.	} 
Fixed Example: 
1.	function processWithdrawal(uint256 value) public {      
2.	    if (balances[msg.sender] > value) {    
3.	        (bool success, ) = msg.sender.seed(value);        
4.	        require(success, "Transfer failed");    
5.	        balances[msg.sender] -= value; }      
6.	} 

Please give me your answer.
(1)
(2)
(3)
(4)
(5)
==================================================================
Case 12:
Here is our suggestion on this case:
Detection result: Yes
Potentially vulnerable code:
function executeProposal(uint _proposalID, bytes _transactionByteCode) public {
        _Proposal storage p = Proposals[_proposalID];
            require(p.recipient.call.value(p.amount)(_transactionByteCode));
Repair Approach: you can fix reentrancy vulnerability by using the "checks-effects-interactions" model.
Vulnerable Example: 
7.	function processWithdrawal(uint256 value) public {    
8.	    if (balances[msg.sender] > value) {  
9.	        (bool success, ) = msg.sender.call.value(value);      
10.	        require(success, "Transfer failed");  
11.	        balances[msg.sender] -= value; }    
12.	} 
Fixed Example: 
1.	function processWithdrawal(uint256 value) public {      
2.	     if (balances[msg.sender] > value) {  
3.	        balances[msg.sender] -= value;  
4.	        (bool success, ) = msg.sender.call.value(value);  
5.	        require(success, "Transfer failed");   
6.	     }      
7.	} 


Please give me your answer.
(1)
(2)
(3)
(4)
(5)

