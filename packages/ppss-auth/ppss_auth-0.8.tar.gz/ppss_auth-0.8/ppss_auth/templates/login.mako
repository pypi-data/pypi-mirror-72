<%inherit file="${context['logintpl']}" />
<div class="container">
    <div class="row text-center">
        <div class="${bc['xs']}12 col-md-4 offset-md-4">
            <form class="my-5" action="${request.route_url('ppsslogin')}" method="POST" class="loginform">
                <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
                <input class="form-control" type="text" name="username" placeholder="username" class="form-control">
                <br/>
                <input class="form-control" type="password" name="password" placeholder="password" class="form-control">
                <br/>
                <div class="text-center">
                    <input class="btn btn-success" type="submit" name="submit" value="Login"/>
                    % if ppsauthconf.newusergroups:
                    <br>
                    <small>Not registered yet? <a href="${request.route_url('ppss:user:register')}">Register now</a></small>
                    % endif
                </div>
                </br>
                <p class="text-danger">${msg}</p>
            </form>
        </div>
    </div>
</div>