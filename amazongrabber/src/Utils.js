import React from "react";
import "./index.css";

const range = len => {
  const arr = [];
  for (let i = 1; i < len -1; i++) {
    arr.push(i);
  }
  return arr;
};

const newReview = (d) => {        
        
    return {

        
        review_id: d[0],
        product_id: d[1],
        review_date: d[2],
        author: d[3],
        rating: parseInt(d[4], 10),
        helpful: parseInt(d[5], 10),
        image_available: parseInt(d[6], 10),
        title: d[7],
        review: d[8],
        link: "https://www.amazon.com"+d[9],
        author_profile: "https://www.amazon.com"+d[10]
    }
}

export function makeData(data) {
  return range(data.length).map(d => {
    return {
      ...newReview(data[d]),
    };
  });
}

export const Logo = () =>
  <div style={{ margin: '1rem auto', display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'center'}}>
    For more examples, visit {''}
  <br />
    <a href="https://github.com/react-tools/react-table" target="_blank">
      <img
        src="https://github.com/react-tools/media/raw/master/logo-react-table.png"
        style={{ width: `150px`, margin: ".5em auto .3em" }}
      />
    </a>
  </div>;

export const Tips = () =>
  <div style={{ textAlign: "center" }}>
    <em>Tip: Hold shift when sorting to multi-sort!</em>
  </div>;
