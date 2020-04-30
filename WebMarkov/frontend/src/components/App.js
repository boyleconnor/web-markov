import React from "react";
import { render } from "react-dom";
import SourceList from './SourceList.js';
import MarkovList from './MarkovList.js';
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
    const markov_url = this.state.markov_url;
    if (markov_url) {
      return (
        <div id="app-interior">
          <MarkovList url={markov_url} />
        </div>
      );
    } else {
      return <p>Loading...</p>
    }
  }
}


export default App;


const container = document.getElementById("app");
render(<App />, container);
