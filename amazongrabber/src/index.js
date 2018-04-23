import React from "react";
import { render } from "react-dom";
import { makeData, Logo, Tips } from "./Utils";
import registerServiceWorker from './registerServiceWorker';
import './index.css';

// Import React Table
import ReactTable from "react-table";
import "react-table/react-table.css";

// Import CSVReader
import CSVReader from "react-csv-reader";

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      data: []
    };
  }

  handleData = data => {
    this.setState({
       data: makeData(data) 
    });
  }

  render() {
    
    return (
        <div>
        <h2>Amazon Review Viewer</h2>
        <p>Display any Amazon Review CSV file as a searchable, filterable, pretty react table.<br />
           Developed by: Anton Foltz</p>
        <CSVReader
          cssClass="react-csv-input"
          label="Select CSV file containing reviews:"
          onFileLoaded={ this.handleData } 
        />

        <ReactTable
          getTdProps={(state, rowInfo, column, instance) => {
            return {
              onClick: (e, handleOriginal) => {
                var url = rowInfo.original[column.id];
                var product = rowInfo.original[column.product_id];
                
                try {
                    var n = url.startsWith("https");
                } catch (e) {
                    console.log('Empty row!');
                }
                
                if (n) {
                    const tab = window.open(url, '_blank');
                    tab.focus();
                }
                
                if (handleOriginal) {
                  handleOriginal();
                }
              }
            };
          }}
          filterable
          defaultFilterMethod={(filter, row) =>
            String(row[filter.id]) === filter.value}
          data={this.state.data}
          columns={[
            {
              Header: "Info",
              columns: [
                {
                  id: "review_id",
                  Header: "Review ID",
                  accessor: "review_id"
                },
                {
                  id: "product_id",
                  Header: "Product ID",
                  accessor: "product_id"
                },
                {
                  id: "review_date",
                  Header: "Review Date",
                  accessor: "review_date"
                },
                {
                  id: "author",
                  Header: "Author",
                  accessor: "author"
                }
              ]
            },
            {
              Header: "Stats",
              columns: [
                {
                  id: "rating",
                  Header: "Rating",
                  accessor: "rating", 
                  Cell: row => (
                  <div
                    style={{
                      width: '100%',
                      height: '100%',
                      backgroundColor: '#dadada',
                      borderRadius: '2px'
                    }}
                  >
                    <div
                      style={{
                        width: `${row.value*20}%`,
                        height: '100%',
                        backgroundColor: row.value*20 > 66 ? '#85cc00'
                          : row.value*20 > 33 ? '#ffbf00'
                          : '#ff2e00',
                        borderRadius: '2px',
                        transition: 'all .2s ease-out'
                      }}
                    />
                  </div>
                  )
                },
                {
                  id: "helpful",
                  Header: "Helpful",
                  accessor: "helpful"
                },
                {
                  Header: "Image Available",
                  accessor: "image_available"
                }
              ]
            },
            {
              Header: 'Review',
              columns: [
                {
                  Header: "Title",
                  accessor: "title"
                },
                {
                  Header: "Review",
                  accessor: "review"
                }
              ]
            },
            {
              Header: 'Links',
              columns: [
                {
                  Header: "Review Link",
                  accessor: "link"
                },
                {
                  Header: "Author Profile",
                  accessor: "author_profile"
                }
              ]
            }
          ]}
          defaultPageSize={20}
          className="-striped -highlight"
        />
        <br />
        <Tips />
        <Logo />
      </div>
    );
  }
}

render(<App />, document.getElementById("root"));
registerServiceWorker();
