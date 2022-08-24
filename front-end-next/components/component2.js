import React from 'react'

import PropTypes from 'prop-types'

const Component2 = (props) => {
  return (
    <>
      <div className="component2-container">
        <button className="component2-button button">{props.button}</button>
      </div>
      <style jsx>
        {`
          .component2-container {
            display: flex;
            position: relative;
          }
          .component2-button {
            transition: 0.3s;
            padding-top: var(--dl-space-space-unit);
            padding-left: 32px;
            padding-right: 32px;
            padding-bottom: var(--dl-space-space-unit);
            background-color: var(--dl-color-gray-white);
          }
          .component2-button:hover {
            color: var(--dl-color-gray-white);
            background-color: var(--dl-color-gray-black);
          }
        `}
      </style>
    </>
  )
}

Component2.defaultProps = {
  button: 'Upload',
}

Component2.propTypes = {
  button: PropTypes.string,
}

export default Component2
