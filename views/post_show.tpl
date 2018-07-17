<!DOCTYPE HTML>
<html>
    <head>
        %include head_common title=title
        <script type="text/javascript">
$(document).ready(function(){
    $('#submit-comment').submit(function() {
        var request = $.ajax({
            type: "POST",
            url: "/comment",
            data: $(this).serialize(),
            dataType: "json"
        })
        
        request.done(function(msg) {
            if(msg.code == "0"){
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
            <h2>{{title}}</h2>
            <div class="comment"><p>Op's Comment Here</p></div>
			<!--comments-->
        %for escaped_comment in escaped_comments:
            <div class="vbox comment-container comment-container-1">
                <div class="comment">{{!escaped_comment}}</div>
            </div>
        %end
            <div class="vbox comment-container comment-container-1">
                <div class="comment">
                    <form id="submit-comment" action="/comment" method="post">
                        <textarea name="text" style="width: 394px; height: 200px"></textarea><br/>
                        <input type="hidden" name="post_id" value="{{post_id}}">
                        <input type="submit" value="Comment" />
                    </form>
                </div>
            </div>
			<!--/comments-->
        </div>
    
        %include menu group_name=group_name, user_name=user_name
    </body>
</html>