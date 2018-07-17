<!DOCTYPE HTML>
<html>
    <head>
        %include head_common title=title
		<script type="text/javascript">
$(document).ready(function(){
    $('#submit-vote').submit(function() {
        var request = $.ajax({
            type: "POST",
            url: "/poll/vote",
            data: $(this).serialize(),
            dataType: "json"
        })
        
        request.done(function(msg) {
            if(msg.code == "0"){
				alert(msg.message);
                location.reload();
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
		<div class="vbox" style="min-width: 420px;">
			<form id="submit-vote" action="/poll/vote" method="post">
				<input type="radio" name="choice" value="1" />Duane's Quest<br />
				<input type="radio" name="choice" value="2" />Rachel's Quest<br />
				<input type="hidden" name="poll_id" value="1">
				<input type="submit" value="Submit">
			</form>
		</div>
		
        %include menu group_name=group_name, user_name=user_name
    </body>
</html>