<%inherit file="/default.mako"/>

<%def name="header()">
    ${head_content}
    
    <link type="text/css" rel="stylesheet" href="/css/demo.css"/>
    
    <!-- Google JS APIs: http://code.google.com/apis/ajaxlibs/ -->
    <script src="http://www.google.com/jsapi"></script>
    <script>
      google.load("jquery", "1.2.6");
      google.load("jqueryui", "1.5.3");
    </script>
</%def>

<%!
    # python code here
%>

<div class="appswell-demo" id="appswell-demo-ajax">

    <div class="controller_menu">
        <h3>menu</h3>
        <ul>
            ${menu}
        </ul>
    </div>

    <h2>ajax example</h2>

    <h5>push a button below to make a ajax request to the
        <a href="/services/dice">services controller</a></h5>
        
    <p id="response">&nbsp;</p>

    <input type="button" class="left" style="width:auto; margin:4px;"
        value="roll a die"
        onclick="javascript:roll_die();" />

    <script>
        function roll_die() {
            var ajax_url = '/services/dice/?callback=?';
            $('#response').html('rolling a 6-sided die...');

            setTimeout(function() {
                $.getJSON( ajax_url, function (json) {
                    if ( json.rolled ) {
                        var die_html = '';
                        if ( json.die != '' ) {
                            die_html = ' ( ' + json.die + ' )';
                        }

                        $('#response').html('rolled a <strong>' +
                                            json.rolled + '</strong>' +
                                            die_html );
                    }
                    else {
                        $('#response').text('request failed');
                    }
                });
            }, 1000)
        }
    </script>

</div>