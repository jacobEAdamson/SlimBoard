        <div style="width: 250px; -webkit-box-flex: 0; -moz-box-flex: 0; box-flex: 0;">
            <div class="vbox" style=" 
                    background-color: #FFFFFF; 
                    box-shadow: 0px 0px 10px black;
                    margin-left: 10px;
                    padding: 10px;">
                <h3>{{group_name}}</h3>
            %if user_name==None:
                <a href="/user/login">Login</a><br/>
            %else:
            	{{user_name}}<br/>
            	<a href="/user/logout">Logout</a><br/>
            %end
                <br/>
                <a href="/">Index</a><br/>
                <a href="/post/create">New Post</a>
            </div>
        </div>