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

var DeleteButton = React.createClass({

  render: function () {

      var onClick = "javascript:delete_service('" + this.props.data.name + "', '" + PUBLIC_KEY + "')";

      return <span>
          <p>Next Alert: { this.props.data.alert }</p>
          No longer using this alert? _
          <a href={onClick}>
            Delete it
          </a>
      </span>
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
            item = this.props.item,
            statusText;

        if (item.passing) {
            listClass += ' service-passing list-group-item-success';
            statusText = 'Passing';
        } else {
            listClass += ' service-failing list-group-item-danger';
            statusText = 'Failing';
        }

        return <li onClick={this.handleClick} className={listClass}>
            <div className="container">
                <div className="row">
                    <div className="col-md-3">
                        {item.name}
                    </div>
                    <div className="col-md-3">
                        <strong>{statusText}</strong>
                    </div>
                    <div className="col-md-3">
                        {item.date}
                    </div>
                    <div className="col-md-3 pull-right">
                        +
                    </div>
                </div>
                { !this.state.collapsed ? <GoogleLineChart data={item}  /> : null }
                { !this.state.collapsed ? <DeleteButton data={item}  /> : null }
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
