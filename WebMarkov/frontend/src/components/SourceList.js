import React from 'react';


class SourceForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filename: "",
    };
    this.fileInput = React.createRef();
  }

  handleChange(event) {
    this.setState({filename: event.target.value});
  }

  handleSubmit() {
    const formData = new FormData();
    console.log(this.fileInput);
    formData.append(
      'source_file',
      this.fileInput.current.files[0],
      this.fileInput.current.files[0].name
    );
    formData.append(
      'name',
      this.state.filename
    );
    formData.append(
      'csrfmiddlewaretoken',
      this.props.csrf
    );
    console.log("Fetching from url: " + this.props.url);
    fetch(this.props.url, {
        method: 'post',
        body: formData
      })
      .then((response) => {
        response.json()
      })
      .then((data) => {
        console.log(data);
        this.props.deleteSelf();
      })
      .catch((exception) => {
        console.log(exception);
      });
  }

  render() {
    return (
      <div className="SourceForm">
        <input type="text" value={this.state.filename} onChange={(e) => this.handleChange(e)} />
        <input type="file" ref={this.fileInput} />
        <button onClick={() => this.handleSubmit()}>Submit</button>
      </div>
    )
  }
}

class SourceList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sources: [],
      showingSourceForm: false,
    };
  }

  fetchSources(url) {
    fetch(url)
      .then(result => result.json())
      .then((data) => {
        this.setState({
          sources: data,
        });
      });
  }

  componentDidMount() {
    this.fetchSources(this.props.url);
  }

  render() {
    const sources = this.state.sources.map((source) => {
      return <li key={source.id}>{source.name}</li>;
    });
    const showingSourceForm = this.state.showingSourceForm;
    if (sources) {
      return (
        <div className="sourcelist">
          <ul>{ sources }<li>CSRF Token: {this.props.csrf}</li></ul>
          {!showingSourceForm
            ? <button onClick={() => this.setState({showingSourceForm: true})} >Add Source</button>
            : <SourceForm
                deleteSelf={() => this.setState({showingSourceForm: false})}
                url={this.props.url} 
                csrf={this.props.csrf}
              />
          }
        </div>
      );
    } else {
      console.log("Loading sources 123");
      return <p>Loading...</p>;
    }
  }
}


export default SourceList;
