import React from "react";
import { render } from "react-dom";
import {NavLink, Route, Switch, BrowserRouter} from "react-router-dom";
import SourceList from './SourceList.js';
import MarkovList from './MarkovList.js';
import MarkovDetail from './MarkovDetail.js';
import About from './About.js';
import Cookies from 'js-cookie';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      source_url: null,
      markov_url: null,
      csrftoken: Cookies.get('csrftoken')  // FIXME: This gets the csrf token from the web host
    };
  }

  fetchUrls() {
    fetch('http://127.0.0.1:8000/api/')
      .then(response => {
        console.table(response);
        return response.json();
      })
      .then(data => this.setState({
        source_url: data.source,
        markov_url: data.markov
      }));
  }

  componentDidMount() {
    this.fetchUrls();
  }

  render() {
    return (
      <BrowserRouter>
        <div id="nav-bar">
          <ul class="nav-bar">
            <li class="nav-list"><NavLink to="/" className="nav-link">Home</NavLink></li>
            <li class="nav-list"><NavLink to="/about/" className="nav-link">About</NavLink></li>
          </ul>
        </div>
      <Switch>
        <Route
          exact
          path="/"
          render={(props) => <MarkovList url={this.state.markov_url} /> }
        />
        <Route
          exact
          path="/about/"
          component={About}
        />
        <Route
          exact
          path="/markov/:markovId"
          render={MarkovDetail}
        />
      </Switch>
      </BrowserRouter>
    );
  }
}


export default App;


const container = document.getElementById("app");
render(<App />, container);
