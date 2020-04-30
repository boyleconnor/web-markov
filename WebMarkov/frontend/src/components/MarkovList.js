import React from "react";


class MarkovDetail extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      random_text: "",
    }
  }

  getRandomText() {
    const markov = this.props.markov;
    fetch(markov.random_text_url)
      .then((response) => response.json())
      .then((data) => this.setState({ random_text: data.random_text }));
  }

  componentDidMount() {
    this.getRandomText();
  }

  render() {
    const markov = this.props.markov;
    const random_text = this.state.random_text;
    return (
      <div className="markov-detail">
        <h3>{markov.name}</h3>
        <p><b>{markov.name}</b> has been trained on the following sources:</p>

        <ul className="training-list">
          {markov.trained_on.map((training) => <li className="trained-source" key={training.source.id}> {training.source.name} </li>)}
        </ul>

        <p>and generated the following text:</p>

        <div className="random-text">
          {this.state.random_text}
        </div>

        <button onClick={() => {this.getRandomText();}}>refresh text</button>
      </div>
    );
  }
}


class MarkovList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      markovs: [],
    }
  }

  fetchMarkovs() {
    fetch(this.props.url)
      .then((response) => response.json())
      .then((data) => 
        this.setState({ markovs: data })
      );
  }

  componentDidMount() {
    this.fetchMarkovs();
  }

  render() {
    const markovs = this.state.markovs;
    let markov_list;
    if (markovs) {
      markov_list = markovs.map((markov) => <MarkovDetail key={markov.id} markov={markov} />);
    } else {
      markov_list = <p>No markovs found</p>;
    }
    return <div className="markov-list">{markov_list}</div>;
  }
}


export default MarkovList;
