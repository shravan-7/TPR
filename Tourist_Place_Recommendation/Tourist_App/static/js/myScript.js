/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function validateUser(){
    var name=document.getElementById('uname').value;
    var contactNo=document.getElementById('contactNo').value;
    var emailId=document.getElementById('emailId').value;
    var address=document.getElementById('address').value;
    var username=document.getElementById('username').value;
    var password=document.getElementById('password').value;
    
    if(name==""){
        window.alert('Please provide Name');
        return false;
    }
    else if(contactNo==""){
        window.alert('Please provide Contact Number');
        return false;
    }
    else if(contactNo.length!=10){
        window.alert('Please provide valid Contact Number');
        return false;
    }
    else if(emailId==""){
        window.alert('Please provide EmailID');
        return false;
    }
    else if(!/(.+)@(.+){2,}\.(.+){2,}/.test(emailId)){
        window.alert('Please provide Valid EmailID');
        return false;
    }
    else if(address==""){
        window.alert('Please provide Address');
        return false;
    }
    else if(username==""){
        window.alert('Please provide Username');
        return false;
    }
    else if(password==""){
        window.alert('Please provide Password');
        return false;
    }
    return true;
}

function validateLogin(){
    var username=document.getElementById('username').value;
    var password=document.getElementById('password').value;
    
    if(username==""){
        window.alert('Please provide Username');
        return false;
    }
    else if(password==""){
        window.alert('Please provide Password');
        return false;
    } 
    return true;
}
