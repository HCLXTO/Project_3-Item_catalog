function renderGplusButton(){
	gapi.signin.render('customBtn', {
      'callback': 'signinCallback',
      'clientid': '362552351555-ch9kmsfn9m6h6lvqh6qivu6fra9m12uq.apps.googleusercontent.com',
      'cookiepolicy': 'single_host_origin',
      //'requestvisibleactions': 'http://schema.org/AddAction',
      'scope': 'openid email',
      'redirecturi':'postmessage',
      'accesstype':'offline',
      'approvalprompt':'force'//remover esse em producao
    });
}
function signinCallback(authResult){
	console.log(authResult);
	if(authResult['code']){
		$('#signinButton').hide();
		$.ajax({
			type:'POST',
			url:'/gconnect?state='+$('#stateHolder').attr('data-state'),
			processData:false,
			contentType: 'application/octet-stream; charset=utf-8',
			data: authResult['code'],
			success: function(result){
				if(result){
					$('#result').html('Login Successfull!</br>'+result+'</br>Redirecting...');
					setTimeout(function(){window.location.href="/"},0);
				}else if(authResult['error']){
					console.log('There was an error: '+authResult['error'])
				}else{
					$('#result').html('Failed to make a server-side call. Check your configuration and console.');
				};
			}
		})
	}
};
// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
	var access_token = FB.getAuthResponse()['accessToken'];
	console.log('statusChangeCallback');
	console.log(response);
	// The response object is returned with a status field that lets the
	// app know the current login status of the person.
	// Full docs on the response object can be found in the documentation
	// for FB.getLoginStatus().
	if (response.status === 'connected') {
		// Logged into your app and Facebook.
		$.ajax({
			type:'POST',
			url:'/fbconnect?state='+$('#stateHolder').attr('data-state'),
			processData:false,
			contentType: 'application/octet-stream; charset=utf-8',
			data: access_token,
			success: function(result){
				if(result){
					$('#result').html('Login Successfull!</br>'+result+'</br>Redirecting...');
					setTimeout(function(){window.location.href="/"},0);
				}else if(authResult['error']){
					console.log('There was an error: '+authResult['error'])
				}else{
					$('#result').html('Failed to make a server-side call. Check your configuration and console.');
				};
			}
		});
	} else if (response.status === 'not_authorized') {
		// The person is logged into Facebook, but not your app.
		document.getElementById('status').innerHTML = 'Please log ' +
		'into this app.';
	} else {
		// The person is not logged into Facebook, so we're not sure if
		// they are logged into this app or not.
		document.getElementById('status').innerHTML = 'Your cookie setting do not' +
		'alow log in with Facebook.';
	}
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
}

window.fbAsyncInit = function() {
	FB.init({
		appId      : '444576199036339',
		cookie     : true,  // enable cookies to allow the server to access 
		    // the session
		xfbml      : true,  // parse social plugins on this page
		version    : 'v2.3' // use version 2.2
	});

	// Now that we've initialized the JavaScript SDK, we call 
	// FB.getLoginStatus().  This function gets the state of the
	// person visiting this page and can return one of three states to
	// the callback you provide.  They can be:
	//
	// 1. Logged into your app ('connected')
	// 2. Logged into Facebook, but not your app ('not_authorized')
	// 3. Not logged into Facebook and can't tell if they are logged into
	//    your app or not.
	//
	// These three cases are handled in the callback function.
	/*
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
	*/
};
function fb_login(){
    FB.login(function(response) {

        if (response.authResponse) {
            statusChangeCallback(response)
        } else {
            //user hit cancel button
            console.log('User cancelled login or did not fully authorize.');
        }
    }, {
        scope: 'public_profile,email,user_friends'
    });
}