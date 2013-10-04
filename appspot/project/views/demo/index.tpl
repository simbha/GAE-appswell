<div class="appswell-demo" id="appswell-demo-index">

    <div class="controller_menu">
        <h3>menu</h3>
        <ul>
            {% autoescape off %}
            {{ menu }}
            {% endautoescape %}
        </ul>
    </div>

    <h2>{{ header }}</h2>

    <h4>{{ subheader|default_if_none:"data" }}</h4>
    
    {% firstof data content %}

</div>