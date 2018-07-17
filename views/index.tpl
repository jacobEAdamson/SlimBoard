<!DOCTYPE HTML>
<html>
    <head>
        %include head_common title=title
    </head>

    <body class="hbox">
    <div>
    %if posts == None:
        There are no posts to display
    %else:
        %for post in posts:
            <h2><a href="/post/show/{{post[0]}}">{{post[1]}}</a></h2>
        %end
    %end
    </div>
        
        %include menu group_name=group_name, user_name=user_name
    </body>
</html>