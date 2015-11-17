var GoogleLineChart = React.createClass({
  render: function(){
    return React.DOM.div({
            id: this.props.data.name.replace(' ', '-'),
            style: {width: '900px', height: '500px', margin: '25px'}
        });
  },
  componentDidMount: function(){
    this.drawCharts();
  },
  componentDidUpdate: function(){
    this.drawCharts();
  },
  drawCharts: function(){
    var data = google.visualization.arrayToDataTable(this.props.data.table);
    var options = {
      trendlines: { 0: {
            labelInLegend: 'Trend line',
            visibleInLegend: true
        }}    // Draw a trendline for data series 0.
    };

    var chart = new google.visualization.LineChart(
      document.getElementById(this.props.data.name.replace(' ', '-'))
    );
    chart.draw(data, options);
  }
});

var ListItem = React.createClass({

  getInitialState: function() {
    return {
      collapsed: true
    };
  },

  handleClick: function(event) {
    this.setState({collapsed: !this.state.collapsed});
    console.log(this.state.collapsed);
  },

   render: function() {

        var listClass = 'service-item list-group-item service',
            item = this.props.item;

        if (item.passing) {
            listClass += ' service-passing list-group-item-success'
        } else {
            listClass += ' service-failing list-group-item-danger'
        }

        return <li onClick={this.handleClick} className={listClass}>
            <div className="container">
                <div className="row">
                    <div className="col-md-3">
                        {item.name}
                    </div>
                    <div className="col-md-3">
                        <strong>Passing</strong>
                    </div>
                    <div className="col-md-3">
                        {item.date}
                    </div>
                    <div className="col-md-3 pull-right">
                        +
                    </div>
                </div>
                { !this.state.collapsed ? <GoogleLineChart data={item}  /> : null }
            </div>
        </li>;
    }
});

var ListItemWrapper = React.createClass({

  getInitialState: function() {
    return {
      data: DATA
    };
  },

  render: function() {

    return <ul className="list-group">
        {this.state.data.map(function(item) {
          return (
            <ListItem key={item.name} item={item} />
          )}
        )}
    </ul>;
  }

});

ReactDOM.render(
  <ListItemWrapper></ListItemWrapper>,
  document.getElementById('ping-list')
);


/*

Last Ping: {{last.create|date:"DATETIME_FORMAT"}}<br>
{% if last.get_closest_alert.notify_at %}
Next Alert: {{last.get_closest_alert.notify_at|date:"DATETIME_FORMAT"}}
{% else %}
<br>
{% endif %}
</div>
<div class="col-md-4">
  <div class="service-controls">
    <u>Details</u> -
    <a href="javascript:delete_service('{{ ping_name.grouper }}', '{{ user.company.public_key }}')"
            style="color:red;">
        Delete</a><br>
  </div>
</div>
*/
