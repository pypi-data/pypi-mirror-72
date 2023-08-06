<div class="ppss_auth--usermanage">
  % if 'user' in request.session:
    Hi <strong>${request.session['user']['name']}</strong><br>
    <small>not ${request.session['user']['name']}? <a href="${request.route_url('ppsslogout')}">Logout</a>
  % else:
    <a href="${request.route_url('ppsslogin')}">Login</a>
  % end if
</div>