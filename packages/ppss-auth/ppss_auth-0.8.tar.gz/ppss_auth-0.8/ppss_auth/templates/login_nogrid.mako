<%inherit file="${context['logintpl']}" />
<form action="${request.route_url('ppsslogin')}" method="POST" class="loginform">
    
    <input class="form-control" type="text" name="username" placeholder="username">
    <br/>
    <input class="form-control" type="password" name="password" placeholder="password">
    <br/>
    <div class="text-center">
        <input class="btn btn-success" type="submit" name="submit" value="entra"/>
    </div>
    </br>
    <p class="text-danger">${msg}</p>
</form>