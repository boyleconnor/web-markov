import React from "react";
import { render } from "react-dom";
import SourceList from './SourceList.js';
import Cookies from 'js-cookie'


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
    const source_url = this.state.source_url;
    if (source_url) {
      return <SourceList url={this.state.source_url} csrf={this.state.csrftoken} />;
    } else {
      return <p>Loading...</p>
    }
  }
}


export default App;


const container = document.getElementById("app");
render(<App />, container);
