import React from 'react'

import PropTypes from 'prop-types'

const Component1 = (props) => {
  return (
    <>
      <div className="component1-container">
        <button className="component1-button button">{props.button}</button>
      </div>
      <style jsx>
        {`
          .component1-container {
            display: flex;
            position: relative;
          }
          .component1-button {
            width: 150px;
            height: 56px;
            background-color: var(--dl-color-gray-white);
          }
        `}
      </style>
    </>
  )
}

Component1.defaultProps = {
  button: 'Upload',
}

Component1.propTypes = {
  button: PropTypes.string,
}

export default Component1
