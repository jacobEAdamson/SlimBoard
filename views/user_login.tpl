<!DOCTYPE HTML>
<html>
    <head>
        %include head_common title='Login Page'
		<script type="text/javascript">
$(document).ready(function(){
    $('#submit-login').submit(function() {
        var request = $.ajax({
            type: "POST",
            url: "/user/login",
            data: $(this).serialize(),
            dataType: "json"
        })
        
        request.done(function(msg) {
            if(msg.code == "0"){
				alert(msg.message);
                window.location.href = '/poll/show/1';
            }
            else{
                alert(msg.message);
            }
        });
        return false;
    });
});
        </script>
    </head>

    <body class="hbox">
    <div>
		<form id="submit-login" action="/user/login" method="post">
			Username: <input type="text" name="username" /><br/>
			Password: <input type="password" name="password" /><br/>
			<input type="submit" value="Login" />
		</form>
    </div>
        
        %include menu group_name=group_name, user_name=user_name
    </body>
</html>