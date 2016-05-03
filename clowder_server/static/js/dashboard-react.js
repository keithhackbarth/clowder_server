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
                No longer using this alert?&nbsp;
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

    dateToString: function (itemDate) {
        var options = {
                year: 'numeric', month: 'long', day: 'numeric',
                hour: '2-digit', minute: '2-digit',
                hour12: false, timeZoneName: 'short'
            },
            dateAsString = new Date(itemDate).toLocaleString('en-US', options);

        return dateAsString;
    },

    render: function() {
        var listClass = 'service-item list-group-item service',
            item = this.props.item,
            statusText,
            dateString = this.dateToString(item.date);

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
                        {dateString}
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

var stateContainer = {
    data: DATA
};

var doSearch = function() {
    var inputVal = document.getElementById('search-input').value,
        searchData = [];

    DATA.map(function(el) {
        var nameLower = el.name.toLowerCase();

        if (nameLower.indexOf(inputVal) !== -1) {
            searchData.push(el);
        }
    });

    stateContainer.data = searchData;
};

var SearchComponent = React.createClass({
    render: function() {
        return <div>
            <div>
                <p className="left search-label">Search</p>
                <input type="text" id="search-input" className="right form-control"
                 placeholder="esc clears input"></input>
            </div>
        </div>;
    }
});

var ListItemWrapper = React.createClass({
    getInitialState: function() {
        return {
            data: stateContainer.data
        };
    },

    updateState: function() {
        var input = document.getElementById('search-input'),
            t = this;

        input.onkeyup = function(e) {
            // If esc key is pressed, clear the input
            // and re-render list. Otherwise render
            // the list, filtering by text input.
            if (e.keyCode === 27) {
                input.value = '';
            }

            // Set the data and set the new state.
            doSearch();
            t.updateListWrapperState();
        };
    },

    updateListWrapperState: function() {
        this.setState({
            data: stateContainer.data
        });
    },

    componentDidMount: function() {
        this.updateState();
    },

    render: function() {
        return <div>
            <ul className="list-group">
                {this.state.data.map(function(item) {
                    return (
                      <ListItem key={item.name} item={item} />
                    )}
                )}
            </ul>
        </div>;
    }
});

ReactDOM.render(
    <SearchComponent/>,
    document.getElementById('search')
);

ReactDOM.render(
    <ListItemWrapper/>,
    document.getElementById('ping-list')
);
